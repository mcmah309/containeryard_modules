```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Rust target for WebAssembly"
requires:
  - path: ./rustup.md
```
```Dockerfile name=main
RUN rustup target add wasm32-unknown-unknown
```
