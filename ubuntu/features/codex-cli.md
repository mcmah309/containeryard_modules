```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "codex-cli"
args:
    optional:
        - no_sandbox
requires:
    - ./curl.md
```
```Dockerfile
RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh
{% if no_sandbox is defined and no_sandbox is not bool %}
    {{ throw(message="no_sandbox must be true or false") }}
{% endif %}

{% set no_sandbox = no_sandbox | default(value=false) %}
{% if no_sandbox %}
RUN mkdir -p /root/.codex \
    && printf '%s\n' \
        'approval_policy = "never"' \
        'sandbox_mode = "danger-full-access"' \
        > /root/.codex/config.toml
{% endif %}
```