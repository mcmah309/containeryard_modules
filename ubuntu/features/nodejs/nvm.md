```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Node version manager"
requires:
    - path: ../curl.md
```
```dockerfile name=main
RUN curl -fsSL --retry 3 https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh -o /tmp/install-nvm.sh \
    && bash /tmp/install-nvm.sh \
    && rm /tmp/install-nvm.sh \
    && . "$HOME/.nvm/nvm.sh" \
    && nvm install --lts \
    && node -v \
    && npm -v \
    && nvm alias default lts/*
```
