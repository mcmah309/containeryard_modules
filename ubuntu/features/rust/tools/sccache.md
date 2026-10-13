```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "compiler caching tool for C/C++, Rust, and Cuda"
requires:
  - path: ../rustup.md
```
```Dockerfile name=build
FROM rustup-builder AS sccache-builder

RUN cargo install sccache --locked
```
```Dockerfile name=main
COPY --from=sccache-builder /usr/local/cargo/bin/sccache /usr/local/cargo/bin/sccache
```
