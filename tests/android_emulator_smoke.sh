#!/bin/sh
# Run inside a container with a booted emulator. No Gradle or network required.
set -eu

sdk=${ANDROID_HOME:?}
platform=${ANDROID_EMULATOR_SYSTEM_IMAGE#system-images;}
platform=${platform%%;*}
android_jar=$sdk/platforms/$platform/android.jar
build_tools=$sdk/build-tools/${ANDROID_BUILD_TOOLS_VERSION:-34.0.0}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
mkdir -p "$work/classes" "$work/dex"

cat > "$work/MainActivity.java" <<'JAVA'
package com.containeryard.smoke;
public class MainActivity extends android.app.Activity {
    @Override public void onCreate(android.os.Bundle state) {
        super.onCreate(state);
        android.widget.TextView text = new android.widget.TextView(this);
        text.setText("Container Yard emulator works");
        text.setTextSize(24);
        setContentView(text);
    }
}
JAVA
cat > "$work/AndroidManifest.xml" <<'MANIFEST'
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.containeryard.smoke">
    <uses-sdk android:minSdkVersion="23" android:targetSdkVersion="34" />
    <application android:label="Container Yard smoke test" android:debuggable="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
MANIFEST

javac -source 8 -target 8 -classpath "$android_jar" -d "$work/classes" "$work/MainActivity.java"
"$build_tools/d8" --lib "$android_jar" --output "$work/dex" \
    "$work/classes/com/containeryard/smoke/MainActivity.class"
"$build_tools/aapt2" link -I "$android_jar" --manifest "$work/AndroidManifest.xml" \
    -o "$work/unsigned.apk"
jar uf "$work/unsigned.apk" -C "$work/dex" classes.dex
"$build_tools/zipalign" -f 4 "$work/unsigned.apk" "$work/aligned.apk"
keytool -genkeypair -keystore "$work/debug.keystore" -storepass android \
    -keypass android -alias androiddebugkey -keyalg RSA -keysize 2048 \
    -validity 1 -dname 'CN=Container Yard smoke test'
"$build_tools/apksigner" sign --ks "$work/debug.keystore" --ks-pass pass:android \
    --out "$work/smoke.apk" "$work/aligned.apk"
adb uninstall com.containeryard.smoke >/dev/null 2>&1 || true
adb install "$work/smoke.apk"
adb shell am start -W -n com.containeryard.smoke/.MainActivity
adb shell dumpsys activity activities | grep '[Rr]esumedActivity.*com.containeryard.smoke'
printf 'Compiled, signed, installed, and launched the smoke app.\n'
