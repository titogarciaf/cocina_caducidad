[app]
title = Cocina Caducidad
package.name = cocina_caducidad
package.domain = org.cocina
source.dir = .
source.include_exts = py,kv,png,jpg,db
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,android,pyjnius,sqlite3
orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

# si tienes service_check.py
services = service_check:service

[android]
android.build_tools_version = 33.0.2
android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS
android.logcat_filter = *:S python:D
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
