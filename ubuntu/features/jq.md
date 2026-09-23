```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "jq JSON processor"
```
```Dockerfile
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    jq \
    && rm -rf /var/lib/apt/lists/*
```
