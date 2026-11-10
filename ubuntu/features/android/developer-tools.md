```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
  Android utils.

  include_emulator installs the emulator, the selected platform's Google APIs
  x86_64 system image, Qt/XCB runtime libraries, and android-emulator launcher.
  The launcher creates an AVD on first use as the current user; no AVD is baked
  into the image. It runs headless without DISPLAY and uses software graphics.
  Graphical operation requires a reachable X11 display and its authentication
  to be supplied at runtime; this module does not start a display server.
  
  Volumes:
  - ${HOME:-/root}/.gradle/caches
  - /opt/android-sdk
  - ${HOME:-/root}/.android/avd (when using the emulator)
args:
  optional:
    - platform
    - build_tools
    - ndk
    - cmake
    - include_emulator
  validate:
    - assert: "include_emulator is not defined or include_emulator is bool"
      message: "include_emulator must be true or false"
requires:
  - path: ./sdk/sdk.md
```
```sh name=install-emulator-launcher
set -eu
cat > /usr/local/bin/android-emulator <<'EMULATOR_LAUNCHER'
#!/bin/sh
set -eu

if [ "${1:-}" = "--help" ]; then
    cat <<'USAGE'
Usage: android-emulator [--headless|--window] [emulator options...]

Creates an AVD on first use, then launches it in the foreground.
Without DISPLAY it runs headless. Pass --window to require an X11 window.
Pass /dev/kvm into the container with --device /dev/kvm.

Environment:
  ANDROID_AVD_NAME    AVD name (default: yard_<installed platform>)
  ANDROID_AVD_DEVICE  Device profile for a new AVD (default: pixel_7)
  ANDROID_AVD_HOME    Writable directory for persistent AVDs
  ANDROID_EMULATOR_GPU     Graphics backend (default: software)
  ANDROID_EMULATOR_MEMORY  RAM in MB (default: 2048)
USAGE
    exit 0
fi

mode=auto
case "${1:-}" in
    --headless) mode=headless; shift ;;
    --window) mode=window; shift ;;
esac
if [ "$mode" = auto ]; then
    if [ -n "${DISPLAY:-}" ]; then mode=window; else mode=headless; fi
fi
if [ "$mode" = window ] && [ -z "${DISPLAY:-}" ]; then
    echo 'android-emulator: window mode requires DISPLAY and a mounted, authenticated X11 socket.' >&2
    exit 1
fi
if [ ! -r /dev/kvm ] || [ ! -w /dev/kvm ]; then
    echo 'android-emulator: /dev/kvm is unavailable. Start the container with --device /dev/kvm; non-root users also need its numeric group via --group-add.' >&2
    exit 1
fi

image=${ANDROID_EMULATOR_SYSTEM_IMAGE:?No emulator system image configured}
platform=${image#system-images;}
platform=${platform%%;*}
name=${ANDROID_AVD_NAME:-yard_$platform}
case "$name" in
    ''|*[!a-zA-Z0-9_.-]*) echo 'android-emulator: invalid ANDROID_AVD_NAME.' >&2; exit 1 ;;
esac
export ANDROID_AVD_HOME=${ANDROID_AVD_HOME:-${ANDROID_USER_HOME:-$HOME/.android}/avd}
mkdir -p "$ANDROID_AVD_HOME"
if [ ! -f "$ANDROID_AVD_HOME/$name.ini" ]; then
    printf 'no\n' | avdmanager create avd --name "$name" --package "$image" \
        --device "${ANDROID_AVD_DEVICE:-pixel_7}"
fi

if [ "$mode" = headless ]; then
    set -- -no-window "$@"
else
    export QT_QPA_PLATFORM=${QT_QPA_PLATFORM:-xcb}
fi
# QtWebEngine requires this when the emulator runs as root. Keep it local to
# the emulator process rather than changing the environment for other apps.
if [ "$(id -u)" -eq 0 ]; then
    export QTWEBENGINE_DISABLE_SANDBOX=1
fi
exec emulator -avd "$name" -accel on -gpu "${ANDROID_EMULATOR_GPU:-software}" \
    -memory "${ANDROID_EMULATOR_MEMORY:-2048}" -no-audio -no-boot-anim -no-snapshot "$@"
EMULATOR_LAUNCHER
chmod 0755 /usr/local/bin/android-emulator
```
```Dockerfile name=main
# https://docs.flutter.dev/reference/supported-platforms
# https://developer.android.com/tools/releases/platform-tools

## For all the latest configs use `sdkmanager --list`

# https://developer.android.com/tools/releases/platforms
# e.g. "android-34"
ARG platform={{ platform | default (value="android-34") }} 
# https://developer.android.com/tools/releases/build-tools
# e.g. "34.0.0"
ARG build_tools={{ build_tools | default (value="34.0.0") }}
# https://developer.android.com/ndk/downloads
ARG ndk={{ ndk | default (value="27.2.12479018") }}
# https://cmake.org/download/ (also check `sdkmanager --list`)
ARG cmake={{ cmake | default (value="3.31.6") }}


# Update the SDK manager and install necessary Android SDK components https://developer.android.com/tools/sdkmanager
RUN sdkmanager --update \
    && sdkmanager \
        # Install the Android SDK for the specified platform version (API level).
        "platforms;${platform}" \
        # Install platform-tools like adb (Android Debug Bridge)
        # This appear to not take a version
        "platform-tools" \
        # Install the specified version of build tools for compiling Android apps
        "build-tools;${build_tools}" \
        # Install the latest version of command-line tools for general SDK management tasks
        "cmdline-tools;latest" \
        ## Extra
        # Install the latest version of the NDK (Native Development Kit) for compiling native code. Cant use "latest" here
        "ndk;${ndk}" \
        # Install the latest version of CMake. Cant use "latest" here
        "cmake;${cmake}"

ENV PATH ${PATH}:${ANDROID_HOME}/emulator
ENV ANDROID_NDK_HOME ${ANDROID_HOME}/ndk/${ndk}
ENV ANDROID_BUILD_TOOLS_VERSION=${build_tools}
# For older envs
ENV NDK_HOME ${ANDROID_NDK_HOME}

{% if include_emulator %}
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxkbfile1 \
        libgl1 \
        libegl1 \
        libpulse0 \
        libnss3 \
        libnspr4 \
        libxcomposite1 \
        libxcursor1 \
        libxi6 \
        libxrandr2 \
        libxtst6 \
        libasound2t64 \
        libsm6 \
        libdrm2 \
        libfontconfig1 \
        fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# `adb kill-server` may be needed.
# `adb start-server` may be needed. `QT_QPA_PLATFORM=` for selecting platform
# Create an AVD at runtime before launching the emulator (see below).
# Headless: `emulator -avd <name> -no-window -no-audio`
# Graphical: `emulator -avd <name> -no-audio` (requires a working X11 display)
RUN sdkmanager "system-images;${platform};google_apis;x86_64" "emulator"
# Some SDK installers leave executable files accessible only to the installer.
# The shared SDK must also be usable by the user who creates the runtime AVD.
RUN chmod -R a+rX "${ANDROID_HOME}/emulator" "${ANDROID_HOME}/system-images/${platform}"
ENV ANDROID_EMULATOR_SYSTEM_IMAGE="system-images;${platform};google_apis;x86_64"
RUN {{ script(name="install-emulator-launcher") }}
RUN emulator -version
{% endif %}
```

With `include_emulator: true`, start a container with KVM access and persistent
AVD storage, then run the launcher. From the host (using this yard's `full` image):

```sh
docker run --rm --device /dev/kvm -v android-avds:/root/.android/avd full android-emulator
```

Inside an existing container with `/dev/kvm` passed through, run
`android-emulator`. The first invocation creates `yard_android-34` (or the
selected platform); subsequent invocations reuse it and retain its app data.
The process stays in the foreground and can be stopped with Ctrl-C.

For an X11 window, also supply `DISPLAY`, mount `/tmp/.X11-unix`, and supply an
Xauthority file that permits the container user to connect. Run
`android-emulator --window`. A Wayland desktop can use its XWayland display.
Use `--headless` to suppress the window even when DISPLAY is set.

`ANDROID_AVD_NAME` and `ANDROID_AVD_DEVICE` select another name/profile.
List profiles with `avdmanager list device`. `ANDROID_AVD_HOME` overrides the
storage location; otherwise it follows `ANDROID_USER_HOME` or `$HOME/.android/avd`.
Non-root users need a writable home/volume and access to the host KVM device
(use `--group-add "$(stat -c %g /dev/kvm)"`). Software graphics do not require a
host GPU mount; `ANDROID_EMULATOR_GPU` can override the backend.

Extra options are forwarded, for example `android-emulator --headless -port 5556`.
In another shell in the same container, use `adb devices` to connect to the
emulator. Wait for `adb shell getprop sys.boot_completed` to return `1` before
installing an app with `adb install app.apk`. This module does not publish ADB
or emulator ports to the host.
