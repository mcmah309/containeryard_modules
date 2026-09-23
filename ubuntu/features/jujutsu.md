```yaml
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
    - ./curl.md
    - ./git.md
```
```Dockerfile

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    {% if not version %}
    jq \
    {% endif %}
    && rm -rf /var/lib/apt/lists/*
RUN \
    {% if version %}
    curl -L -o jj.tar.gz https://github.com/jj-vcs/jj/releases/download/{{ version }}/jj-{{ version }}-x86_64-unknown-linux-musl.tar.gz \
    {% else %}
    DOWNLOAD_URL=$(curl -s https://api.github.com/repos/jj-vcs/jj/releases/latest | jq -r '.assets[] | select(.name | test("x86_64-unknown-linux-musl")) | .browser_download_url') \
    && curl -L -o jj.tar.gz "$DOWNLOAD_URL" \
    {% endif %}
    && tar -xvzf jj.tar.gz \
    && mv jj /usr/local/bin/ \
    && rm jj.tar.gz \
    && jj --version
RUN \
    jj config set --user user.name {{ user_name }} \
    && jj config set --user user.email {{ email }}
```
