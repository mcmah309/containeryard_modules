```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
    Docker CLI with Buildx and Compose, using an external Docker daemon.

    Mount the host socket at /var/run/docker.sock when starting the container:
      --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock

    For a rootless host daemon, mount its socket at the same container destination.
    Non-root container users need the socket's numeric group ID via --group-add.
    DOCKER_HOST can select another socket or a remote daemon.
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && . /etc/os-release \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        docker-ce-cli \
        docker-buildx-plugin \
        docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*
```
