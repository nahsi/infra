#!/usr/bin/env python3
"""Consolidate, then refresh stale mental models one at a time.

Models must have Hindsight's own refresh triggers disabled: they start every
model at once, which overloads the embedding server.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request

BANK = os.environ["HINDSIGHT_API_URL"].rstrip("/") + "/v1/default/banks/personal"
HEADERS = {
    "Authorization": f"Bearer {os.environ['HINDSIGHT_API_KEY']}",
    "Content-Type": "application/json",
}
ACTIVE = ("pending", "processing")


def log(event, **fields):
    print(json.dumps({"event": event, **fields}), flush=True)


def call(path, payload=None):
    request = urllib.request.Request(
        BANK + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers=HEADERS,
        method="GET" if payload is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def wait(operation_id):
    while (status := call(f"/operations/{operation_id}")["status"]) in ACTIVE:
        time.sleep(15)
    return status


def main():
    log("consolidating", operation_id=call("/consolidate", {})["operation_id"])
    # A consolidation round enqueues the next one, so re-list until none are left.
    while ids := [op["id"] for status in ACTIVE
                  for op in call(f"/operations?type=consolidation&status={status}&limit=100")["operations"]]:
        for operation_id in ids:
            wait(operation_id)

    failed = []
    for model in call("/mental-models?detail=metadata&limit=1000")["items"]:
        if not model["is_stale"]:
            continue
        operation_id = call(f"/mental-models/{urllib.parse.quote(model['id'], safe='')}/refresh", {})["operation_id"]
        status = wait(operation_id)
        log("refreshed", model=model["id"], operation_id=operation_id, status=status)
        if status != "completed":
            failed.append(model["id"])
    log("completed", failed=failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
