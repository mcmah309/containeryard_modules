```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "codex-desktop"
requires:
    - ./curl.md
```
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        dbus \
        dbus-x11 \
        xdg-desktop-portal \
        xdg-desktop-portal-gtk \
    && curl --proto '=https' --tlsv1.2 -fL --retry 3 \
        -o /tmp/chatgpt_amd64.deb \
        https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_amd64.deb \
    && apt-get install -y --no-install-recommends \
        /tmp/chatgpt_amd64.deb \
    && rm -f /tmp/chatgpt_amd64.deb \
    && rm -rf /var/lib/apt/lists/*
RUN printf '%s\n' \
        '#!/bin/sh' \
        'set -eu' \
        'exec /usr/bin/chatgpt --no-sandbox --ozone-platform=x11 --disable-dev-shm-usage "$@"' \
        > /usr/local/bin/codex-desktop \
    && chmod 0755 /usr/local/bin/codex-desktop \
    && mkdir -p /root/.local/share/applications \
    && sed 's|^Exec=.*|Exec=/usr/local/bin/codex-desktop %U|' \
        /usr/share/applications/chatgpt.desktop \
        > /root/.local/share/applications/chatgpt.desktop
```
