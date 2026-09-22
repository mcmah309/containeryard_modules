```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "compiler caching tool for C/C++, Rust, and Cuda"
requires:
  - ../rustup.md
```
```Dockerfile
RUN cargo install sccache --locked
```
