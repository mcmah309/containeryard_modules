```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Jekyll package for Ruby. Requires Ruby."
requires:
    - path: ./ruby.md
```
```Dockerfile name=main
RUN gem install jekyll bundler
```
