```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "claude-cli"
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN curl -fsSL https://claude.ai/install.sh | bash
```
