```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Activate rust crate"
args:
  optional:
    - add_bashrc_shortcut
  validate:
    - assert: "add_bashrc_shortcut is not defined or add_bashrc_shortcut is bool"
      message: "add_bashrc_shortcut must be true or false"
requires:
  - path: ../rustup.md
```
```Dockerfile name=main
RUN cargo install activate {% if add_bashrc_shortcut %} && echo 'a() { eval "$(activate "$@")"; }' >> ~/.bashrc {% endif %}
```
