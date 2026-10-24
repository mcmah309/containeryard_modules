```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Stripe Cli"
requires:
    - path: ./curl.md
    - path: ./gpg.md
```
```Dockerfile name=main
RUN curl -fsSL --retry 3 https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public -o /tmp/stripe-key.pub \
    && gpg --dearmor -o /usr/share/keyrings/stripe.gpg /tmp/stripe-key.pub \
    && rm /tmp/stripe-key.pub \
    && echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | tee -a /etc/apt/sources.list.d/stripe.list \
    && apt-get update \
    && apt-get install -y stripe \
    && rm -rf /var/lib/apt/lists/*
```
