```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
  Podman in Podman.

  Volumes:
  - /var/lib/containers #  Root podman containers location. (For users ~/.local/share/containers)
```
```Dockerfile name=main
# Podman in Podman
# Tips:
# - Run outer with with `--privileged`
# Known issues: 
# - some containers may need args like `--net=host` on the inside and outside container


RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    podman \
    && rm -rf /var/lib/apt/lists/* \
    && tee /etc/containers/registries.conf > /dev/null <<EOF
[registries]
[registries.block]
registries = []

[registries.insecure]
registries = []

[registries.search]
registries = ["docker.io", "quay.io"]
EOF
```
