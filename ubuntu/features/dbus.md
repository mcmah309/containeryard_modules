```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "D-Bus session support"
args:
    required:
        - register_startup_hook
```
```Dockerfile
{% if register_startup_hook is not bool %}
    {{ throw(message="register_startup_hook must be true or false") }}
{% endif %}

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        dbus \
        dbus-x11 \
    && rm -rf /var/lib/apt/lists/*
ENV DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-session
{% if register_startup_hook %}
RUN mkdir -p /usr/local/lib/containeryard/startup.d \
    && printf '%s\n' \
        '#!/bin/sh' \
        'set -eu' \
        '' \
        'rm -f /tmp/dbus-session' \
        'dbus-daemon --session --address="$DBUS_SESSION_BUS_ADDRESS" --fork' \
        > /usr/local/lib/containeryard/startup.d/50-dbus-session \
    && chmod 0755 /usr/local/lib/containeryard/startup.d/50-dbus-session
{% endif %}
```
