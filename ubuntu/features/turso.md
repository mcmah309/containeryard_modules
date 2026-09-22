```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "turso cli tools"
requires:
    - ./curl.md
```
```Dockerfile
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*
# Turso CLI (Mainly cloud operations)
RUN curl -sSfL https://get.tur.so/install.sh | bash
# Turso interactive SQL shell (db operations)
RUN curl --proto '=https' --tlsv1.2 -LsSf https://github.com/tursodatabase/turso/releases/download/v0.6.0-pre.21/turso_cli-installer.sh | sh
```
