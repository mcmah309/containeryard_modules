```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "bash interactive module with mcmah309 flavor and useful tools"
required_files:
  - setup_bash.sh
requires:
  - ../../curl.md
```
```Dockerfile
COPY ./setup_bash.sh /tmp/
RUN chmod +x /tmp/setup_bash.sh && /tmp/setup_bash.sh && rm /tmp/setup_bash.sh
```
