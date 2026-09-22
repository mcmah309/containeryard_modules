```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "copilot-cli"
requires:
    - ./curl.md
```
```Dockerfile
RUN curl -fsSL https://gh.io/copilot-install | bash
```
