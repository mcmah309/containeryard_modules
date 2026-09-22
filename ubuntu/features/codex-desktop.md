```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "codex-desktop"
requires:
    - ./curl.md
    - ./dbus.md
    - ./xdg.md
```
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && curl --proto '=https' --tlsv1.2 -fL --retry 3 \
        -o /tmp/chatgpt_amd64.deb \
        https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_amd64.deb \
    && apt-get install -y --no-install-recommends \
        /tmp/chatgpt_amd64.deb \
    && rm -f /tmp/chatgpt_amd64.deb \
    && rm -rf /var/lib/apt/lists/*
RUN printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        '' \
        'if [[ -z "${DISPLAY:-}" ]]; then' \
        '    echo '"'"'DISPLAY is unset. Pass the host DISPLAY and mount /tmp/.X11-unix into the container.'"'"' >&2' \
        '    exit 1' \
        fi \
        '' \
        '# Reuse the container session bus, or create a private bus for this launch.' \
        'if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" && -S /tmp/dbus-session ]]; then' \
        '    export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-session' \
        fi \
        'if ! dbus-send --session --print-reply --reply-timeout=2000 \' \
        '    --dest=org.freedesktop.DBus /org/freedesktop/DBus \' \
        '    org.freedesktop.DBus.ListNames >/dev/null 2>&1; then' \
        '    exec dbus-run-session -- "$0" "$@"' \
        fi \
        '' \
        'desktop_args=(--ozone-platform=x11 --disable-dev-shm-usage)' \
        '# Chromium refuses to run as root without this flag.' \
        'if (( EUID == 0 )); then' \
        '    desktop_args+=(--no-sandbox)' \
        fi \
        'exec /usr/bin/chatgpt "${desktop_args[@]}" "$@"' \
        > /usr/local/bin/codex-desktop \
    && chmod 0755 /usr/local/bin/codex-desktop \
    && mkdir -p /root/.local/share/applications \
    && sed 's|^Exec=.*|Exec=/usr/local/bin/codex-desktop %U|' \
        /usr/share/applications/chatgpt.desktop \
        > /root/.local/share/applications/chatgpt.desktop
```
