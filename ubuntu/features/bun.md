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
RUN curl -fsSL https://bun.com/install | bash {% if version %} -s "{{ version }}" {% endif %}
```
