```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
    Flutter module

    Volumes:
    - /dev/bus/usb # debugging on real device
    - ${HOME:-/root}/.pub-cache # Dart pub cache
args:
  optional:
    - flutter_version
requires:
  - ../curl.md
  - ../android/sdk/sdk.md
  - ../xdg.md
```
```Dockerfile
ARG flutter_ver={{ flutter_version | default (value="3.27.3") }}

## Set environment variables
ENV FLUTTER_HOME=/usr/local/flutter
ENV PATH ${PATH}:${FLUTTER_HOME}/bin:${FLUTTER_HOME}/bin/cache/dart-sdk/bin:${HOME:-/root}/.pub-cache/bin

# Needed for linux, sets x11 to use the first display, use `export GDK_BACKEND=wayland` to use wayland
ENV DISPLAY=:0

RUN mkdir -p $FLUTTER_HOME \
## Base linux config
    && apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests ca-certificates \
    && update-ca-certificates \

## Install base tools required flutter tools https://docs.flutter.dev/get-started/install/linux#system-requirements
    && apt-get install -y --no-install-recommends --no-install-suggests \
    bash \
    file \
    git \
    # mkdir \
    # rm \
    unzip \
    # which \
    xz-utils \
    zip \

## For linux desktop apps: https://docs.flutter.dev/get-started/install/linux#linux-prerequisites
    && apt-get install -y --no-install-recommends --no-install-suggests \
    clang \
    cmake \
    git \
    ninja-build \
    pkg-config \
    libgtk-3-dev \
    liblzma-dev \
    libstdc++-12-dev \

## Linux downloads https://docs.flutter.dev/release/archive?tab=linux
## Download Flutter, extract it to the FLUTTER_HOME directory, and then remove the original file
    && curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${flutter_ver}-stable.tar.xz \
    && tar xf flutter_linux_${flutter_ver}-stable.tar.xz -C $FLUTTER_HOME --strip-components=1 \
    && rm flutter_linux_${flutter_ver}-stable.tar.xz \

## `flutter config` fails without this
    && git config --global --add safe.directory /usr/local/flutter \

## Setup Flutter
    && flutter config --enable-android \
                --enable-linux-desktop \
                --enable-web \
                --enable-ios \
                --enable-macos-desktop \
                --enable-windows-desktop \

## Pre-fetch Flutter development binaries
    && flutter precache --universal \
    --linux \
    --web \
    --ios \
    --macos \
    --windows \

## Accept Android licenses
    && yes | flutter doctor --android-licenses \

## Linux
### Install Chrome (Used by Flutter Web)
    && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \

## Create a google chrome executable that allows running as root. Used by flutter when lauching web apps.
    && ORIGINAL_CHROME_PATH=$(which google-chrome) \
    && mv "$ORIGINAL_CHROME_PATH" "${ORIGINAL_CHROME_PATH}-bin" \
    && echo '#!/bin/bash\n'"${ORIGINAL_CHROME_PATH}-bin"' --no-sandbox --headless "$@"' > /usr/bin/google-chrome \
    && chmod +x /usr/bin/google-chrome \

    && rm -rf /var/lib/apt/lists/*
```
