```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Tailwind cli"
requires:
    - ./nvm.md
```
```Dockerfile
RUN . ~/.bashrc  && { nvm use default 2>/dev/null || true; } && npm install -g tailwindcss @tailwindcss/cli
```

https://tailwindcss.com/docs/installation/tailwind-cli

Note: tailwind v4 requires each project to install it's own tailwind `npm install tailwindcss @tailwindcss/cli`

Daisy install: https://daisyui.com/docs/install/
