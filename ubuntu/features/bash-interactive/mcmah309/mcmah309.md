```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "bash interactive module with mcmah309 flavor and useful tools"
files:
  - path: setup_bash.sh
requires:
  - path: ../../curl.md
```
```Dockerfile name=main
COPY ./setup_bash.sh /tmp/
RUN chmod +x /tmp/setup_bash.sh && /tmp/setup_bash.sh && rm /tmp/setup_bash.sh
```
