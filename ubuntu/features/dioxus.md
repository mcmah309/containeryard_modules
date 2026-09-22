```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Dioxus. Also depends on cargo being installed."
args:
    optional:
    - version # e.g. `0.6.0-alpha.4` do not include the `v`
requires:
    - ./rust/rustup.md
    - ./curl.md
```
```Dockerfile
# From: https://dioxuslabs.com/learn/0.7/getting_started
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    libwebkit2gtk-4.1-dev \
    build-essential \
    wget \
    file \
    libxdo-dev \
    libssl-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    && rm -rf /var/lib/apt/lists/*
RUN cargo install cargo-binstall --locked \
    && cargo binstall dioxus-cli {% if version %} --version {{version}} --force {% endif %}
```
