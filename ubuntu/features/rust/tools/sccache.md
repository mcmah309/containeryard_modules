```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "compiler caching tool for C/C++, Rust, and Cuda"
requires:
  - ../rustup.md
split: true
```
```Dockerfile
FROM rustup-builder AS sccache-builder

RUN cargo install sccache --locked
```
```Dockerfile
COPY --from=sccache-builder /usr/local/cargo/bin/sccache /usr/local/cargo/bin/sccache
```
