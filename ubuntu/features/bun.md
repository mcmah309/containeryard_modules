```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Bun"
args:
    optional:
        - version # e.g. `bun-v1.2.19`
requires:
    - ./curl.md
    - ./unzip.md
```
```Dockerfile
RUN curl -fsSL https://bun.com/install | bash {% if version %} -s "{{ version }}" {% endif %}
```
