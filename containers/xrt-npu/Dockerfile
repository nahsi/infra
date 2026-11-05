ARG DEBIAN_IMAGE=debian:trixie-slim@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2
ARG XRT_VERSION=1:2.25.0-4~bpo13+1

FROM ${DEBIAN_IMAGE}
ARG DEBIAN_IMAGE
ARG XRT_VERSION

RUN echo "deb http://deb.debian.org/debian trixie-backports main" > /etc/apt/sources.list.d/backports.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends -t trixie-backports \
      libxrt2="${XRT_VERSION}" libxrt-npu2="${XRT_VERSION}" \
 && rm -rf /var/lib/apt/lists/*

LABEL org.opencontainers.image.title="XRT NPU runtime" \
      org.opencontainers.image.source="https://github.com/nahsi/infra" \
      org.opencontainers.image.version="${XRT_VERSION}" \
      org.opencontainers.image.base.name="${DEBIAN_IMAGE}"
