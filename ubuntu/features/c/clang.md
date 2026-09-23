```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "clang development module"
args:
    optional:
        - version
requires:
    - ../wget.md
    - ../gpg.md
```
```Dockerfile
{% if version %}
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    lsb-release \
    software-properties-common \
    && wget https://apt.llvm.org/llvm.sh \
    && chmod +x llvm.sh \
    && ./llvm.sh {{ version }} \
    && rm ./llvm.sh \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    clang-{{ version }} \
    clangd-{{ version }} \
    clang-tools-{{ version }} \
    clang-format-{{ version }} \
    clang-tidy-{{ version }} \
    lldb-{{ version }} \
    lld-{{ version }} \
    # Core Tool Symlinks
    && ln -s /usr/bin/clang-{{ version }} /usr/local/bin/clang \
    && ln -s /usr/bin/clangd-{{ version }} /usr/local/bin/clangd \
    && ln -s /usr/bin/clang-format-{{ version }} /usr/local/bin/clang-format \
    && ln -s /usr/bin/clang-tidy-{{ version }} /usr/local/bin/clang-tidy \
    && ln -s /usr/bin/lldb-{{ version }} /usr/local/bin/lldb \
    && ln -s /usr/bin/lld-{{ version }} /usr/local/bin/lld \
    # Additional Tools from 'clang-tools' and 'clang-{{ version }}' Symlinks
    && ln -s /usr/bin/clang-apply-replacements-{{ version }} /usr/local/bin/clang-apply-replacements \
    && ln -s /usr/bin/clang-check-{{ version }} /usr/local/bin/clang-check \
    && ln -s /usr/bin/clang-rename-{{ version }} /usr/local/bin/clang-rename \
    && ln -s /usr/bin/c-index-test-{{ version }} /usr/local/bin/c-index-test \
    && ln -s /usr/bin/scan-build-{{ version }} /usr/local/bin/scan-build \
{% else %}
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    clang \
    clangd \
    clang-tools \
    clang-format \
    clang-tidy \
    lldb \
    lld \
{% endif %}
    && rm -rf /var/lib/apt/lists/*
```
