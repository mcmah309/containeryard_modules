From: https://github.com/thyrlian/AndroidSDK/blob/317b2273b6a4bb15e1219b3386f4a9e3b81a8245/android-sdk/Dockerfile

```yaml name=config
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Android sdk dev env"
# args:
#   optional:
files:
    - path: accredited-keys/.gitignore
    - path: license-accepter.sh
    - path: sshd-banner
    - path: supervisord.conf
requires:
    - path: ../../git.md
    - path: ../../wget.md
    - path: ../../unzip.md
```

```Dockerfile name=main
# install Java
# install essential tools
ARG JDK_VERSION=17
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends openjdk-${JDK_VERSION}-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# download and install Gradle
# https://services.gradle.org/distributions/
ARG GRADLE_VERSION=8.10.2
ARG GRADLE_DIST=bin
RUN cd /opt && \
    wget -q https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-${GRADLE_DIST}.zip && \
    unzip gradle*.zip && \
    ls -d */ | sed 's/\/*$//g' | xargs -I{} mv {} gradle && \
    rm gradle*.zip

# download and install Kotlin compiler
# https://github.com/JetBrains/kotlin/releases/latest
ARG KOTLIN_VERSION=2.0.20
RUN cd /opt && \
    wget -q https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/kotlin-compiler-${KOTLIN_VERSION}.zip && \
    unzip *kotlin*.zip && \
    rm *kotlin*.zip

# download and install Android SDK
# https://developer.android.com/studio#command-line-tools-only
ARG ANDROID_SDK_VERSION=11076708
ENV ANDROID_HOME=/opt/android-sdk
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    unzip *tools*linux*.zip -d ${ANDROID_HOME}/cmdline-tools && \
    mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/tools && \
    rm *tools*linux*.zip

# set the environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-${JDK_VERSION}-openjdk-amd64
ENV GRADLE_HOME=/opt/gradle
ENV KOTLIN_HOME=/opt/kotlinc
ENV PATH=${PATH}:${GRADLE_HOME}/bin:${KOTLIN_HOME}/bin:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/cmdline-tools/tools/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator
# accept the license agreements of the SDK components
ADD license-accepter.sh /opt/
RUN chmod +x /opt/license-accepter.sh && /opt/license-accepter.sh $ANDROID_HOME

# setup adb server
EXPOSE 5037

# install and configure SSH server
EXPOSE 22
ADD sshd-banner /etc/ssh/
ADD accredited-keys /tmp/
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server supervisor locales && \
    mkdir -p /var/run/sshd /var/log/supervisord && \
    locale-gen en en_US en_US.UTF-8 && \
    apt-get remove -y locales && apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    FILE_SSHD_CONFIG="/etc/ssh/sshd_config" && \
    echo "\nBanner /etc/ssh/sshd-banner" >> $FILE_SSHD_CONFIG && \
    echo "\nPermitUserEnvironment=yes" >> $FILE_SSHD_CONFIG && \
    ssh-keygen -q -N "" -f /root/.ssh/id_rsa && \
    FILE_SSH_ENV="/root/.ssh/environment" && \
    touch $FILE_SSH_ENV && chmod 600 $FILE_SSH_ENV && \
    printenv | grep "JAVA_HOME\|GRADLE_HOME\|KOTLIN_HOME\|ANDROID_HOME\|LD_LIBRARY_PATH\|PATH" >> $FILE_SSH_ENV && \
    echo "\nauth required pam_env.so envfile=$FILE_SSH_ENV" >> /etc/pam.d/sshd && \
    FILE_AUTH_KEYS="/root/.ssh/authorized_keys" && \
    touch $FILE_AUTH_KEYS && chmod 600 $FILE_AUTH_KEYS && \
    for file in /tmp/*.pub; \
    do if [ -f "$file" ]; then echo "\n" >> $FILE_AUTH_KEYS && cat $file >> $FILE_AUTH_KEYS && echo "\n" >> $FILE_AUTH_KEYS; fi; \
    done && \
    (rm /tmp/*.pub 2> /dev/null || true)

ADD supervisord.conf /etc/supervisor/conf.d/
```
