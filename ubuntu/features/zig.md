```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Installs zigup and zig"
args:
    optional:
        - version
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    xz-utils \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL --retry 3 https://github.com/marler8997/zigup/releases/latest/download/zigup-x86_64-linux.tar.gz -o /tmp/zigup.tar.gz \
    && tar xzf /tmp/zigup.tar.gz -C /usr/local/bin \
    && rm /tmp/zigup.tar.gz \
    && /usr/local/bin/zigup {{ version | default (value="0.16.0") }} --install-dir /usr/local/bin
```
