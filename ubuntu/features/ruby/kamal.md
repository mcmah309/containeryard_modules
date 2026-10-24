```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Kamal deployment CLI. Uses Docker and Buildx with an external Docker daemon."
requires:
    - path: ./ruby.md
    - path: ../docker.md
    - path: ../git.md
    - path: ../openssh-client.md
```
```Dockerfile name=main
RUN gem install kamal --no-document
```
