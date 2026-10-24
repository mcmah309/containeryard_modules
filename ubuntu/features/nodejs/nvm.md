```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Node version manager"
requires:
    - path: ../curl.md
```
```dockerfile name=main
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh | bash \
    && . "$HOME/.nvm/nvm.sh" \
    && nvm install --lts \
    && node -v \
    && npm -v \
    && nvm alias default lts/*
```
