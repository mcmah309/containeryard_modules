```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "hurl module"
args:
    optional:
        - version
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN VERSION={{ version | default (value="6.0.0") }} \
    && curl --fail --show-error --location --retry 3 --remote-name https://github.com/Orange-OpenSource/hurl/releases/download/$VERSION/hurl_${VERSION}_amd64.deb \
    && apt install ./hurl_${VERSION}_amd64.deb \
    && rm ./hurl_${VERSION}_amd64.deb
```
