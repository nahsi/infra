ARG DEBIAN_IMAGE=debian:trixie-slim@sha256:8aa5a7bf5a1955bddbe7d74fcdd0b91ab30e74362a8b73af672b0481b35b44a0
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
