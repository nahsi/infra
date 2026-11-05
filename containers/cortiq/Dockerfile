# syntax=docker/dockerfile:1.27
ARG UBUNTU_IMAGE=ubuntu:26.04@sha256:6a06111c3b0a8600feadb270aec771dc239bf407b25625f93f44ab00e11f4d3c

FROM ${UBUNTU_IMAGE} AS runtime
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
      ca-certificates \
      curl \
      ffmpeg \
      libgomp1 \
      libvulkan1 \
      mesa-vulkan-drivers=26.0.8-1ubuntu0.3 \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /models \
 && chown 65532:65532 /models

FROM runtime AS download
ADD --checksum=sha256:f28131e6343dd29a5d476dd422d87f92c42d510c556e2c38edb17af09f297864 \
    https://github.com/infosave2007/cmf/releases/download/v0.8.57/cortiq-x86_64-unknown-linux-gnu.tar.gz /tmp/cortiq.tar.gz
RUN tar -xzf /tmp/cortiq.tar.gz -C /usr/local/bin cortiq \
 && chmod 0555 /usr/local/bin/cortiq

FROM runtime
ARG UBUNTU_IMAGE
LABEL org.opencontainers.image.title="Cortiq" \
      org.opencontainers.image.source="https://github.com/nahsi/infra" \
      org.opencontainers.image.version="0.8.57" \
      org.opencontainers.image.base.name="${UBUNTU_IMAGE}"
COPY --from=download /usr/local/bin/cortiq /usr/local/bin/cortiq
ENV HOME=/models \
    XDG_CACHE_HOME=/models/.cache \
    XDG_RUNTIME_DIR=/tmp
WORKDIR /models
USER 65532:65532
EXPOSE 8080
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/cortiq"]
CMD ["--help"]
