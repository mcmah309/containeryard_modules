```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Stripe Cli"
requires:
    - ./curl.md
```
```Dockerfile
RUN curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | tee /usr/share/keyrings/stripe.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | tee -a /etc/apt/sources.list.d/stripe.list \
    && apt-get update \
    && apt-get install -y stripe \
    && rm -rf /var/lib/apt/lists/*
```
