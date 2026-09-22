```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "XDG desktop integration"
```
```Dockerfile
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        xdg-desktop-portal \
        xdg-desktop-portal-gtk \
        xdg-user-dirs \
    && rm -rf /var/lib/apt/lists/*
```
