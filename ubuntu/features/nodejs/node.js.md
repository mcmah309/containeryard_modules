```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Node.js"
args:
    optional:
        - version
requires:
    - path: ../curl.md
```
```Dockerfile name=main
# set to 4, 5, 6, ... as needed
RUN v={{ version | default (value="24") }} \
    && curl -fsSL --retry 3 https://deb.nodesource.com/setup_$v.x -o /tmp/install-nodesource.sh \
    && bash /tmp/install-nodesource.sh \
    && rm /tmp/install-nodesource.sh \
    && apt install nodejs \
    && node -v \
    && npm -v \
    && npx -v \
    && rm -rf /var/lib/apt/lists/*
```
