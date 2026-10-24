```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Base ubuntu module."
args:
  optional:
    - version
```
```Dockerfile name=main
FROM ubuntu:{{ version | default (value="latest") }}

ENV HOME=/root

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```
