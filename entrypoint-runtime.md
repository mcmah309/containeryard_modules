```yaml name=config
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
    image ENTRYPOINT; the consuming output can redeclare the CMD.
```
```Dockerfile name=main
RUN mkdir -p /usr/local/bin /usr/local/lib/containeryard/startup.d \
    && printf '%s\n' \
        '#!/bin/sh' \
        'set -eu' \
        '' \
        'LOG_FILE=/tmp/containeryard-startup.log' \
        '' \
        'log() {' \
        '    printf "[containeryard] %s\n" "$*" | tee -a "$LOG_FILE" >&2' \
        '}' \
        '' \
        'log "Entrypoint started"' \
        '' \
        'for startup_script in /usr/local/lib/containeryard/startup.d/*; do' \
        '    [ -x "$startup_script" ] || continue' \
        '' \
        '    log "Running: $startup_script"' \
        '' \
        '    if "$startup_script" >> "$LOG_FILE" 2>&1; then' \
        '        log "Finished: $startup_script"' \
        '    else' \
        '        status=$?' \
        '        log "Failed: $startup_script (exit code $status)"' \
        '        exit "$status"' \
        '    fi' \
        'done' \
        '' \
        'log "Startup hooks completed"' \
        '' \
        '[ "$#" -gt 0 ] || {' \
        '    log "No container command was configured"' \
        '    exit 64' \
        '}' \
        '' \
        'exec "$@"' \
        > /usr/local/bin/containeryard-entrypoint \
    && chmod 0755 /usr/local/bin/containeryard-entrypoint

ENTRYPOINT ["/usr/local/bin/containeryard-entrypoint"]
CMD ["sleep", "infinity"]
```
