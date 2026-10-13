```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "c development essentials module"
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    # Core C development headers and libc
    libc6-dev \
    # Metadata for discovering library compile/link flags
    pkg-config \
    # Essential binary utilities (ar, nm, objdump, strip, etc.)
    binutils \
    # GCC, g++, dpkg-dev, and other standard build tools (optional but increases compatibility)
    build-essential \
    # Documentation for libc
    # manpages-dev \
    && rm -rf /var/lib/apt/lists/*
```