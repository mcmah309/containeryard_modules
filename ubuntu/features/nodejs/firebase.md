```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Firebase cli module. Needs Node.js."
requires:
    - ./nvm.md
```
```Dockerfile
RUN . ~/.bashrc  && { nvm use default 2>/dev/null || true; } && npm install -g firebase-tools
```

Users can then run `firebase login` to setup for their project
