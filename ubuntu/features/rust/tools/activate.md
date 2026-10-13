```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Activate rust crate"
args:
  optional:
    - add_bashrc_shortcut
requires:
  - path: ../rustup.md
```
```Dockerfile name=main
RUN cargo install activate {% if add_bashrc_shortcut %} && echo 'a() { eval "$(activate "$@")"; }' >> ~/.bashrc {% endif %}
```
