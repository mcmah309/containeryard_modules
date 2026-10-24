```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
    jujustu version control (jj). https://github.com/jj-vcs/jj/releases
args:
    required:
        - user_name
        - email
    optional:
        - version # e.g `v0.35.0`
requires:
    - path: ./curl.md
    - path: ./git.md
    - path: ./jq.md
      when: "version is not defined or not version"
```
```Dockerfile name=main

RUN \
    {% if version -%}
    curl -fsSL --retry 3 -o jj.tar.gz https://github.com/jj-vcs/jj/releases/download/{{ version }}/jj-{{ version }}-x86_64-unknown-linux-musl.tar.gz \
    {% else -%}
    curl -fsSL --retry 3 https://api.github.com/repos/jj-vcs/jj/releases/latest -o /tmp/jj-release.json \
    && DOWNLOAD_URL=$(jq -er '.assets[] | select(.name | test("x86_64-unknown-linux-musl")) | .browser_download_url' /tmp/jj-release.json) \
    && rm /tmp/jj-release.json \
    && curl -fsSL --retry 3 -o jj.tar.gz "$DOWNLOAD_URL" \
    {% endif -%}
    && tar -xvzf jj.tar.gz \
    && mv jj /usr/local/bin/ \
    && rm jj.tar.gz \
    && jj --version
RUN \
    jj config set --user user.name {{ user_name }} \
    && jj config set --user user.email {{ email }}
```
