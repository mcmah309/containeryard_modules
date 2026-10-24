```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "copilot-cli"
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://gh.io/copilot-install -o /tmp/install-copilot.sh \
    && bash /tmp/install-copilot.sh \
    && rm /tmp/install-copilot.sh \
    && copilot --version
```
