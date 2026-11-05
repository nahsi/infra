# syntax=docker/dockerfile:1.27
ARG UBUNTU_IMAGE=ubuntu:26.04@sha256:6a06111c3b0a8600feadb270aec771dc239bf407b25625f93f44ab00e11f4d3c
ARG RUST_IMAGE=rust@sha256:bc2c4c21d4467cdbbac0ee7b95a6deb742a3467dfe0ff7647916c4b42ca56372
ARG CORTIQ_REPO=https://github.com/infosave2007/cmf.git
ARG CORTIQ_REV=811a646c42a3ffda9df02ce96acc0d03f18b8f75

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

FROM ${RUST_IMAGE} AS build
ARG CORTIQ_REPO
ARG CORTIQ_REV
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends glslc=2025.2-1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /src/cmf
RUN git init . \
 && git remote add origin "${CORTIQ_REPO}" \
 && git fetch --depth=1 origin "${CORTIQ_REV}" \
 && git checkout --detach FETCH_HEAD \
 && test "$(git rev-parse HEAD)" = "${CORTIQ_REV}"

RUN --mount=type=bind,source=.,target=/patches \
    git apply /patches/*.patch \
 && for k in d1_q8_quant d1_q8_dp4a d1_attn_coop; do \
      glslc --target-env=vulkan1.3 -O -o "crates/cortiq-engine/src/gpu_wgpu/$k.spv" "crates/cortiq-engine/src/gpu_wgpu/$k.comp"; \
    done

RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/src/cmf/target \
    cargo build --release --locked -p cortiq-cli --features gpu,phonon \
 && install -m 0555 target/release/cortiq /usr/local/bin/cortiq

FROM runtime
ARG UBUNTU_IMAGE
LABEL org.opencontainers.image.title="Cortiq" \
      org.opencontainers.image.source="https://github.com/nahsi/infra" \
      org.opencontainers.image.version="0.8.57-nahsilabs.2" \
      org.opencontainers.image.base.name="${UBUNTU_IMAGE}"
COPY --from=build /usr/local/bin/cortiq /usr/local/bin/cortiq
ENV HOME=/models \
    XDG_CACHE_HOME=/models/.cache \
    XDG_RUNTIME_DIR=/tmp
WORKDIR /models
USER 65532:65532
EXPOSE 8080
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/cortiq"]
CMD ["--help"]
