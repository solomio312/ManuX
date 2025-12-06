# ManuX Wealth OS - Android

Versiune Android a aplicației ManuX Wealth OS construită cu **Kivy** și **KivyMD**.

## 📱 Caracteristici Android

- **UI Material Design** - Interfață elegantă și intuitivă
- **8 Module complete** - Calculator, Monte Carlo, Coș Lunar, FIRE, Imobiliar, Rebalansare, Taxe, Ghid
- **API ECB** - Cursuri valutare fără dependențe problematice
- **Build automat** - GitHub Actions generează APK

## 🚀 Build Local

### Cerințe
```bash
pip install kivy kivymd requests pillow buildozer
```

### Test local (fără Android)
```bash
cd android
python main.py
```

### Build APK
```bash
cd android
buildozer android debug
```

APK-ul va fi în folderul `android/bin/`.

## 📂 Structură

```
android/
├── main.py              # Entry point
├── buildozer.spec       # Config build Android
├── requirements.txt     # Dependențe Python
├── screens/
│   ├── home.py          # Ecran principal (8 butoane)
│   ├── calculator.py    # Calculator investiții
│   ├── monte_carlo.py   # Simulare Monte Carlo  
│   ├── basket.py        # Coș lunar România
│   ├── fire.py          # Simulator FIRE
│   ├── real_estate.py   # Calculator imobiliar
│   ├── rebalance.py     # Rebalansare portofoliu
│   ├── tax.py           # Calculator taxe
│   └── guide.py         # Ghid investiții
├── utils/
│   └── currency.py      # API ECB cursuri
└── assets/
    └── logo.png
```

## 🔄 GitHub Actions

Workflow-ul `android-build.yml` rulează automat la push în folderul `android/`.

APK-ul poate fi descărcat din **Artifacts** sau **Releases** (la tag).
