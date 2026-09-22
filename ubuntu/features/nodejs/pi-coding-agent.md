```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "pi coding agent"
requires:
    - ./nvm.md
```
```Dockerfile
RUN . ~/.bashrc  && { nvm use default 2>/dev/null || true; } && npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```
