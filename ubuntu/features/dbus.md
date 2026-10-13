```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "D-Bus session support"
args:
    required:
        - register_startup_hook
    validate:
        - assert: "register_startup_hook is bool"
          message: "register_startup_hook must be true or false"
requires:
    - path: ../../entrypoint-runtime.md
      when: "register_startup_hook == true"
```
```sh name=install-startup-hook
set -eu
mkdir -p /usr/local/lib/containeryard/startup.d
cat > /usr/local/lib/containeryard/startup.d/50-dbus-session <<'DBUS_STARTUP_SCRIPT'
#!/bin/sh
set -eu

rm -f /tmp/dbus-session
dbus-daemon --session --address="$DBUS_SESSION_BUS_ADDRESS" --fork
DBUS_STARTUP_SCRIPT
chmod 0755 /usr/local/lib/containeryard/startup.d/50-dbus-session
```
```Dockerfile name=main
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        dbus \
        dbus-x11 \
    && rm -rf /var/lib/apt/lists/*
ENV DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-session
{% if register_startup_hook %}
RUN {{ script(name="install-startup-hook") }}
{% endif %}
```
