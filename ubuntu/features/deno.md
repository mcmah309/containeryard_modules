```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Deno"
args:
    optional:
        - version # e.g. `1.0.1`
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://deno.land/install.sh -o /tmp/install-deno.sh \
    && sh /tmp/install-deno.sh --yes \
    && rm /tmp/install-deno.sh \
    && /root/.deno/bin/deno --version {% if version %} && /root/.deno/bin/deno upgrade --version {{ version }} {% endif %}
```
