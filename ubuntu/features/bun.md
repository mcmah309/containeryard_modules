```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Bun"
args:
    optional:
        - version # e.g. `bun-v1.2.19`
requires:
    - path: ./curl.md
    - path: ./unzip.md
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://bun.com/install -o /tmp/install-bun.sh \
    && bash /tmp/install-bun.sh {% if version %} "{{ version }}" {% endif %} \
    && rm /tmp/install-bun.sh \
    && /root/.bun/bin/bun --version
```
