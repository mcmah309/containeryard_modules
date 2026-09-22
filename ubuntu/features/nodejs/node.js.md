```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Node.js"
args:
    optional:
        - version
requires:
    - ../curl.md
```
```Dockerfile
# set to 4, 5, 6, ... as needed
RUN v={{ version | default (value="24") }} \
    && curl -sL https://deb.nodesource.com/setup_$v.x | bash - \
    && apt install nodejs \
    && node -v \
    && npm -v \
    && npx -v \
    && rm -rf /var/lib/apt/lists/*
```
