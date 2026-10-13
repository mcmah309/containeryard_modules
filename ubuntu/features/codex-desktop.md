```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
    Installs Codex Desktop.

    Runtime requirements:
      - Forward DISPLAY and mount /tmp/.X11-unix for X11.
      - Provide /dev/dri for hardware-accelerated graphics.
      - When using Wayland, forward WAYLAND_DISPLAY and XDG_RUNTIME_DIR, and
        mount XDG_RUNTIME_DIR at the same path inside the container.

    The launcher defaults to automatic display backend selection without an
    Ozone platform flag. Set display_backend to x11 or wayland to require a
    specific display backend.
args:
    optional:
        - display_backend
    validate:
        - assert: 'display_backend is not defined or display_backend in ["auto", "x11", "wayland"]'
          message: "display_backend must be auto, x11, or wayland"
requires:
    - path: ./curl.md
    - path: ./dbus.md
    - path: ./xdg.md
```
```bash name=install-launcher
set -euo pipefail
{% set display_backend = display_backend | default(value="auto") %}
cat > /usr/local/bin/codex-desktop <<'CODEX_DESKTOP_LAUNCHER'
#!/usr/bin/env bash
set -euo pipefail

{% if display_backend == "wayland" %}
if [[ -z "${WAYLAND_DISPLAY:-}" || -z "${XDG_RUNTIME_DIR:-}" ]]; then
    echo 'WAYLAND_DISPLAY and XDG_RUNTIME_DIR are unset. Pass both host variables and mount XDG_RUNTIME_DIR at the same path inside the container.' >&2
    exit 1
fi
{% elif display_backend == "x11" %}
if [[ -z "${DISPLAY:-}" ]]; then
    echo 'DISPLAY is unset. Pass the host DISPLAY and mount /tmp/.X11-unix into the container.' >&2
    exit 1
fi
{% else %}
if [[ -z "${DISPLAY:-}" && ( -z "${WAYLAND_DISPLAY:-}" || -z "${XDG_RUNTIME_DIR:-}" ) ]]; then
    echo 'No usable display environment was found. Configure either DISPLAY for X11, or WAYLAND_DISPLAY and XDG_RUNTIME_DIR for Wayland.' >&2
    exit 1
fi
{% endif %}

# Reuse the container session bus, or create a private bus for this launch.
if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" && -S /tmp/dbus-session ]]; then
    export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-session
fi
if ! dbus-send --session --print-reply --reply-timeout=2000 \
    --dest=org.freedesktop.DBus /org/freedesktop/DBus \
    org.freedesktop.DBus.ListNames >/dev/null 2>&1; then
    exec dbus-run-session -- "$0" "$@"
fi

desktop_args=(--disable-dev-shm-usage)
{% if display_backend != "auto" %}
desktop_args+=(--ozone-platform={{ display_backend }})
{% endif %}
# Chromium refuses to run as root without this flag.
if (( EUID == 0 )); then
    desktop_args+=(--no-sandbox)
fi
exec /usr/bin/chatgpt "${desktop_args[@]}" "$@"
CODEX_DESKTOP_LAUNCHER
chmod 0755 /usr/local/bin/codex-desktop
mkdir -p /root/.local/share/applications
sed 's|^Exec=.*|Exec=/usr/local/bin/codex-desktop %U|' \
    /usr/share/applications/chatgpt.desktop \
    > /root/.local/share/applications/chatgpt.desktop
```
```dockerfile name=main
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
RUN {{ script(name="install-launcher", template=true) }}
```
