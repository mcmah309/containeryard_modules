```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Ubuntu module with cuda."
```
```Dockerfile name=main
FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

ENV HOME ${HOME:-/root}

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```