```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Rust components like rustfmt"
args:
  optional:
    - components
requires:
  - ./rustup.md
split: true
```
```Dockerfile
FROM rustup-builder AS rust-components-builder

RUN rustup component add {{ components | default (value="rustfmt clippy") }}
```
```Dockerfile
COPY --from=rust-components-builder /usr/local/rustup /usr/local/rustup
COPY --from=rust-components-builder /usr/local/cargo /usr/local/cargo
```
