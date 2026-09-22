```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: |
  Android utils.
  
  Volumes:
  - ${HOME:-/root}/.gradle/caches
  - /opt/android-sdk
args:
  optional:
    - platform
    - build_tools
    - ndk
    - cmake
    - include_emulator
requires:
  - ./sdk/sdk.md
```
```Dockerfile
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
# For older envs
ENV NDK_HOME ${ANDROID_NDK_HOME}

{% if include_emulator %}
# `adb kill-server` may be needed.
# `adb start-server` may be needed. `QT_QPA_PLATFORM=` for selecting platform
# Run emulator e.g. `emulator -avd pixel_7_33 -no-audio`
RUN sdkmanager "system-images;${platform};google_apis;x86_64" "emulator" \
  && avdmanager create avd -n pixel_7 -k "system-images;${platform};google_apis;x86_64" --device "pixel_7"
{% endif %}
```
