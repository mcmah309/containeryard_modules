```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Rust targets for Android"
requires:
  - ./rustup.md
```
```Dockerfile
# https://dioxuslabs.com/learn/0.6/guides/mobile/

# aarch64-linux-android: Modern Android devices (64-bit ARM)
# armv7-linux-androideabi: Older Android devices (32-bit ARM)
# i686-linux-android: Intel/x86 Android devices (32-bit, uncommon)
# x86_64-linux-android: Intel/x86 Android devices (64-bit, very rare)
RUN rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android
```
