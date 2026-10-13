```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Essential packages for rust development like openssl"
```
```Dockerfile name=main
# libssl-dev: Needed for openssl certificates (may need to add the pkg files to PKG_CONFIG_PATH)
# libasound2-dev: Needed for alsa (may need to add the pkg files to PKG_CONFIG_PATH)
# pkg-config: Quering local libraries for compilation. Needed by rustc.
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    libssl-dev \
    libasound2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
```
