```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
  git module

  Volumes:
  - ${HOME:-/root}:/.ssh
args:
  required:
    - user_name
    - email
requires:
  - path: ./openssh-client.md
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN \
    git config --global user.name {{ user_name }} \
    && git config --global user.email {{ email }} \
    # Make pull, checkout, and switch automatically update submodules
    && git config --global submodule.recurse true
```
