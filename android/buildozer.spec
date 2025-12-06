[app]
title = ManuX Wealth OS
package.name = manuxwealthos
package.domain = com.manux
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 16.2.0
requirements = python3,kivy==2.3.0,kivymd==2.0.1.dev0,requests,pillow

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

# Icon and presplash
icon.filename = assets/logo.png
presplash.filename = assets/logo.png

# Build
fullscreen = 0
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
