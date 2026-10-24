```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "codex-cli"
args:
    optional:
        - no_sandbox
        - notify
    validate:
        - assert: "no_sandbox is not defined or no_sandbox is bool"
          message: "no_sandbox must be true or false"
        - assert: "notify is not defined or notify is bool"
          message: "notify must be true or false"
requires:
    - path: ./curl.md
    - path: ./dbus.md
      when: "notify is defined and notify == true"
```
```sh name=configure
set -eu
mkdir -p /root/.codex
cat > /root/.codex/config.toml <<'CODEX_CONFIG'
tui.alternate_screen = "never"
{% if no_sandbox is defined and no_sandbox == true %}
approval_policy = "never"
sandbox_mode = "danger-full-access"
{% endif %}
{% if notify is defined and notify == true %}
notify = ["sh", "-c", "notify-send \"Codex\" \"Turn complete\""]
{% endif %}
CODEX_CONFIG
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://chatgpt.com/codex/install.sh -o /tmp/install-codex.sh \
    && CODEX_NON_INTERACTIVE=1 CODEX_INSTALL_DIR=/usr/local/bin sh /tmp/install-codex.sh \
    && rm /tmp/install-codex.sh \
    && codex --version
{% if notify is defined and notify == true %}
RUN apt-get update \
    && apt-get install -y --no-install-recommends libnotify-bin \
    && rm -rf /var/lib/apt/lists/*
{% endif %}
RUN {{ script(name="configure", template=true) }}
```
