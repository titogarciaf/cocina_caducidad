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

# punto de entrada por defecto es main.py; no hace falta entrypoint

# Arquitecturas y APIs
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

# Servicio Python (si tienes service_check.py en la raíz)
services = service_check:service

[android]
# build-tools exacto para que el aidl coincida con el SDK del workflow
android.build_tools_version = 33.0.2

# Permisos (los mismos que en p4a.extra_args si quieres duplicarlos)
android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS

# (opcional) logs más limpios en ejecución
android.logcat_filter = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
