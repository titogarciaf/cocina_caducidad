[app]

# (str) Title of your application
title = Cocina Caducidad

# (str) Package name
package.name = cocina_caducidad

# (str) Package domain (unique identifier)
package.domain = org.cocina

# (str) Source code where main.py is located
source.dir = .

# (list) Extensions to include in the APK
source.include_exts = py,png,jpg,kv,atlas,db,json,sqlite3

# (str) Application versioning (e.g., 1.0.0)
version = 1.0.0

# (list) Application requirements
# Nota: kivymd 1.2.0 es estable; no usar 2.x porque cambia la API.
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,android,pyjnius,sqlite3

# (str) Preset app entry point
entrypoint = main.py

# (int) Target Android API (SDK version)
android.api = 33

# (int) Minimum supported Android API
android.minapi = 24

# (list) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# (str) Android build tools version (muy importante para compatibilidad con aidl)
android.build_tools_version = 33.0.2

# (str) Orientation of the app (portrait or landscape)
orientation = portrait

# (str) Full screen mode
fullscreen = 1

# (str) Application icon
icon.filename = assets/icon.png

# (bool) Include the database file in the APK
android.include_sqlite3 = True

# (bool) Enable Android logcat for debugging
log_level = 2

# (bool) Use Android service
services = service_check:service

# (str) Permissions required by your app
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK,ACCESS_NETWORK_STATE,ACCESS_NOTIFICATION_POLICY,POST_NOTIFICATIONS

# (list) Presplash screen image
presplash.filename = assets/presplash.png

# (list) Presplash color (if image not available)
presplash.color = #ffffff

# (str) Supported screen orientations (portrait|landscape|sensor)
orientation = portrait

# (str) Package format
package.format = apk

# (bool) Sign the APK automatically (debug key)
android.release_artifact = True

# (bool) Include launcher icons
android.add_presplash = True

# (str) Additional arguments for the Python for Android (p4a) build
p4a.extra_args = --permission=RECEIVE_BOOT_COMPLETED --permission=WAKE_LOCK --permission=ACCESS_NOTIFICATION_POLICY --permission=POST_NOTIFICATIONS

# (str) Android NDK path (GitHub Actions lo define automáticamente)
# android.ndk_path = /home/runner/work/cocina_caducidad/cocina_caducidad/android-sdk/ndk/25.2.9519653

# (str) Android SDK path (GitHub Actions lo define automáticamente)
# android.sdk_path = /home/runner/work/cocina_caducidad/cocina_caducidad/android-sdk

# (str) Extra Java options
java.compile_options = -source 11 -target 11

# (bool) Optimize APK
android.strip = True

# (bool) Include compiled libraries
android.add_libs_armeabi = True

# (bool) Enable multitouch
use_multiprocessing = True


[buildozer]

# (str) Log level (0 = quiet, 1 = normal, 2 = verbose)
log_level = 2

# (str) Output directory for the built APKs
bin_dir = bin

# (bool) Clean previous builds automatically
clean_build = False

# (str) Directory for local .buildozer folder
build_dir = .buildozer

# (str) Enable verbose output
verbose = True

# (str) Default command to execute
default_command = android debug


[android]

# (str) Target build tools version
android.build_tools_version = 33.0.2

# (str) API level for build
android.api = 33

# (str) Minimum API level supported
android.minapi = 24

# (bool) Allow android logcat
android.logcat_filter = *:S python:D

# (str) Android NDK version (GitHub Actions instala 25.2.9519653)
android.ndk = 25.2.9519653

# (bool) Allow Internet access
android.allow_backup = True

# (str) Name of the compiled APK
android.release_filename = cocina_caducidad.apk
