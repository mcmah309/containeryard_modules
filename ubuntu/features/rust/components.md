```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Rust components like rustfmt"
args:
  optional:
    - components
requires:
  - ./rustup.md
```
```Dockerfile
RUN rustup component add {{ components | default (value="rustfmt clippy") }}
```
