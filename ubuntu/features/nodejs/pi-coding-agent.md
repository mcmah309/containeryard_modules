```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "pi coding agent"
requires:
    - path: ./nvm.md
```
```Dockerfile name=main
RUN . ~/.bashrc  && { nvm use default 2>/dev/null || true; } && npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```
