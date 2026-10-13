```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "unzip"
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    unzip \
    && rm -rf /var/lib/apt/lists/*
```
