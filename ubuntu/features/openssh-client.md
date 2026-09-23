```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "OpenSSH client tools"
```
```Dockerfile
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*
```
