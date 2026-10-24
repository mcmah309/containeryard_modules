```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "claude-cli"
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://claude.ai/install.sh -o /tmp/install-claude.sh \
    && bash /tmp/install-claude.sh \
    && rm /tmp/install-claude.sh \
    && /root/.local/bin/claude --version
```
