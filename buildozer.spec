[app]
title = Caducidad cocina
package.name = cocina_caducidad
package.domain = org.tuempresa   # cámbialo si quieres
source.dir = .
source.include_exts = py,kv,db,png,jpg,ttf
version = 0.1.0
orientation = portrait
fullscreen = 0

# Importante: dependencias
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,android,pyjnius,sqlite3

# API Android (33 = Android 13)
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

# Servicio Python en segundo plano
services = service_check:service

# Icono opcional
# icon.filename = %(source.dir)s/icon.png

[android]
android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS

[buildozer]
log_level = 2
warn_on_root = 1
