ARG DEBIAN_IMAGE=debian:trixie-slim@sha256:f6b08b09a05725f9431502d3b5714f5c4576e82c1a84fa1debe0c24a7e0c3ec4
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
