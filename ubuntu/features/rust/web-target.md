```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Rust target for WebAssembly"
requires:
  - ./rustup.md
```
```Dockerfile
RUN rustup target add wasm32-unknown-unknown
```
