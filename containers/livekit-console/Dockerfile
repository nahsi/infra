FROM scratch AS source
ADD https://github.com/unpod-ai/livekit-console.git#00e6db3af102914db2c65e339c11fcefa0807edb /src/

FROM node:26-alpine@sha256:8996bb5821d62a8fd9bb27c1cb07462f3fdce6e47d640c6a881ead0b064ce216 AS build
WORKDIR /app
COPY --from=source /src/package.json /src/package-lock.json ./
COPY --from=source /src/server/package.json server/
COPY --from=source /src/web/package.json web/
RUN npm ci
COPY --from=source /src/ ./
RUN npm run build

FROM node:26-alpine@sha256:8996bb5821d62a8fd9bb27c1cb07462f3fdce6e47d640c6a881ead0b064ce216
WORKDIR /app
ENV NODE_ENV=production
LABEL org.opencontainers.image.source="https://github.com/unpod-ai/livekit-console" \
      org.opencontainers.image.revision="00e6db3af102914db2c65e339c11fcefa0807edb" \
      org.opencontainers.image.version="0.1.0"
COPY --from=source /src/package.json /src/package-lock.json ./
COPY --from=source /src/server/package.json server/
COPY --from=source /src/web/package.json web/
RUN npm ci --omit=dev -w server
COPY --from=build /app/server/dist server/dist
COPY --from=build /app/web/dist web/dist
USER 10000:10000
EXPOSE 8080
CMD ["node", "server/dist/index.js"]
