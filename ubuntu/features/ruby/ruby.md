```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Ruby module"
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    ruby-full \
    build-essential \
    zlib1g-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*
ENV GEM_HOME=${HOME:-/root}/gems
ENV PATH=${GEM_HOME}/bin:${PATH}
```
