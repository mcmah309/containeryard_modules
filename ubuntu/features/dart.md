```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Dart module"
args:
  optional:
    - dart_version
    - channel
```
```Dockerfile name=main
# https://dart.dev/get-dart#install-a-debian-package

ARG dart_ver={{ dart_version | default (value="3.6.2") }}

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    wget \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://storage.googleapis.com/dart-archive/channels/{{ channel | default (value="stable") }}/release/${dart_ver}/linux_packages/dart_${dart_ver}-1_amd64.deb \
    && dpkg -i dart_${dart_ver}-1_amd64.deb \
    && rm dart_${dart_ver}-1_amd64.deb

ENV PATH ${PATH}:${HOME:-/root}/.pub-cache/bin
```
