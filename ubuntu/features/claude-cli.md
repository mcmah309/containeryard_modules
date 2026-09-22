```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "claude-cli"
requires:
    - ./curl.md
```
```Dockerfile
RUN curl -fsSL https://claude.ai/install.sh | bash
```
