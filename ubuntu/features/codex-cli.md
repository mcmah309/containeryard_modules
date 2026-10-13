```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "codex-cli"
args:
    optional:
        - no_sandbox
        - notify # This requires the dbus feature. Containeryard 0.5.0 can handle this
requires:
    - path: ./curl.md
```
```Dockerfile name=main
RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh
{% if no_sandbox is defined and no_sandbox is not bool %}
    {{ throw(message="no_sandbox must be true or false") }}
{% endif %}

{% set no_sandbox = no_sandbox | default(value=false) %}
RUN mkdir -p /root/.codex \
    && printf '%s\n' \
        'tui.alternate_screen = "never"' \
        {% if no_sandbox %}
        'approval_policy = "never"' \
        'sandbox_mode = "danger-full-access"' \
        {% endif %}
        {% if notify is defined and notify %}
        'notify = ["sh", "-c", "notify-send \"Codex\" \"Turn complete\""]' \
        {% endif %}
    > /root/.codex/config.toml
```
