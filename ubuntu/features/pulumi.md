```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Pulumi CLI"
args:
    optional:
        - version # e.g. `3.273.0`; defaults to the latest release
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL --retry 3 https://get.pulumi.com -o /tmp/install-pulumi.sh \
    && sh /tmp/install-pulumi.sh --no-edit-path {% if version %} --version "{{ version }}" {% endif %} \
    && rm /tmp/install-pulumi.sh
ENV PATH="${HOME}/.pulumi/bin:${PATH}"
RUN pulumi version
```
