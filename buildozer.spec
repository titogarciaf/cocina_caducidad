[app]
title = Cocina Caducidad
package.name = cocina_caducidad
package.domain = org.tito
source.dir = .
source.include_exts = py,kv,db
version = 0.1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,android,pyjnius,sqlite3
orientation = portrait
fullscreen = 0
log_level = 2

# Si usas una base de datos/archivo inicial:
# assets = db.sqlite3

[buildozer]
log_level = 2
warn_on_root = 1

# Fuerza p4a master (coincide con el workflow)
p4a.branch = master

# Arquitecturas típicas
arch = arm64-v8a,armeabi-v7a

# API min/target
android.minapi = 24
android.api = 33

# Bootstrap recomendado para Kivy
android.bootstrap = sdl2

# Usa el SDK/NDK que preparamos en el workflow
android.sdk_path = $ANDROID_SDK_ROOT
android.ndk_path = $ANDROID_NDK_HOME

# Build-tools y cmdline-tools ya están en PATH por el workflow
