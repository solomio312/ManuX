[app]
title = ManuX Wealth OS
package.name = manuxwealthos
package.domain = com.manux
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 16.2.0
requirements = python3,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,requests,pillow

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a
p4a.branch = v2024.01.21

# Icon and presplash
icon.filename = assets/logo.png
presplash.filename = assets/logo.png

# Build
fullscreen = 0
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
