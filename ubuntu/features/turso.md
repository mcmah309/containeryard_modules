```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "turso cli tools"
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*
# Turso CLI (Mainly cloud operations)
RUN curl -fsSL --retry 3 https://get.tur.so/install.sh -o /tmp/install-turso-cloud.sh \
    && bash /tmp/install-turso-cloud.sh \
    && rm /tmp/install-turso-cloud.sh \
    && /root/.turso/turso --version
# Turso interactive SQL shell (db operations)
RUN curl --proto '=https' --tlsv1.2 -LsSf --retry 3 https://github.com/tursodatabase/turso/releases/download/v0.6.0-pre.21/turso_cli-installer.sh -o /tmp/install-turso-sql.sh \
    && sh /tmp/install-turso-sql.sh \
    && rm /tmp/install-turso-sql.sh \
    && /root/.turso/tursodb --version
```
