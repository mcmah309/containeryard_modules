```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "uv for python and project management"
args:
    optional:
        - version # e.g. 0.5.18
requires:
    - path: ../curl.md
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN \
{% if version %}
    curl -LsSf --retry 3 https://astral.sh/uv/{{ version }}/install.sh -o /tmp/install-uv.sh \
{% else %}
    curl -LsSf --retry 3 https://astral.sh/uv/install.sh -o /tmp/install-uv.sh \
{% endif %}
    && sh /tmp/install-uv.sh \
    && rm /tmp/install-uv.sh \
    && "$HOME/.local/bin/uv" --version
```
