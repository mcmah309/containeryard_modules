```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "python module with most of the needed tools for development"
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    libssl-dev \
    pkg-config \
    python3-full \
    python3-dev \
    pipx \
    && rm -rf /var/lib/apt/lists/* \
    && pipx ensurepath \
    && ln -s /usr/bin/python3 /usr/bin/python
```