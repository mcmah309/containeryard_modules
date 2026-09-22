```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
    Installs a container entrypoint that runs composable startup scripts before the
    configured container command.

    Before starting the container command, the entrypoint executes every executable
    file in /usr/local/lib/containeryard/startup.d in filename order. Startup scripts
    receive no command arguments and must exit successfully after completing their
    initialization. A failing script stops container startup.

    This allows independent modules to initialize services and other runtime state
    without defining competing ENTRYPOINT instructions. Including this module sets the
    image ENTRYPOINT; the consuming output remains responsible for declaring CMD.
```
```Dockerfile
RUN mkdir -p /usr/local/lib/containeryard/startup.d \
    && printf '%s\n' \
        '#!/bin/sh' \
        'set -eu' \
        '' \
        'for startup_script in /usr/local/lib/containeryard/startup.d/*; do' \
        '    [ -x "$startup_script" ] || continue' \
        '    "$startup_script"' \
        'done' \
        '' \
        '[ "$#" -gt 0 ] || {' \
        '    echo "No container command was configured" >&2' \
        '    exit 64' \
        '}' \
        '' \
        'exec "$@"' \
        > /usr/local/bin/containeryard-entrypoint \
    && chmod 0755 /usr/local/bin/containeryard-entrypoint
ENTRYPOINT ["/usr/local/bin/containeryard-entrypoint"]
```
