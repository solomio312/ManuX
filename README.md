# ManuX Wealth OS Enterprise 16.2

![ManuX Wealth OS](logo.png)

**Simulator avansat pentru proiecții financiare și planificare investiții**

[![Build](https://github.com/solomio312/ManuX/actions/workflows/build.yml/badge.svg)](https://github.com/solomio312/ManuX/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🚀 Funcționalități

| Modul | Descriere |
|-------|-----------|
| 🧮 **Calculator** | Proiecție investiții cu dobândă compusă |
| 🎲 **Monte Carlo** | Simulare 10,000 scenarii cu volatilitate |
| 🛒 **Coș Lunar** | Cheltuieli minime România 2024-2025 |
| 🔥 **FIRE** | Simulator pensie (regula 4%) |
| 🏠 **Imobiliar** | Calculator ROI investiții imobiliare |
| ⚖️ **Rebalansare** | Ajustare portofoliu |
| 💸 **Taxe** | Calculator taxe România / Canada / SUA |
| 📚 **Ghid** | Educație financiară pentru începători |

---

## 📦 Instalare

### Din surse (dezvoltare)

```bash
git clone https://github.com/solomio312/ManuX.git
cd ManuX
pip install -r requirements.txt
python main_app.py
```

### Executabil (Release)

Descarcă ultima versiune din [Releases](https://github.com/solomio312/ManuX/releases):
- **Windows**: `ManuX-Windows.exe`
- **macOS**: `ManuX-macOS.app`
- **Linux**: `ManuX-Linux`

---

## 🛠️ Dezvoltare

### Structura proiectului

```
ManuX/
├── main_app.py          # Aplicația principală
├── theme_styles.py      # Teme și stiluri
├── widgets.py           # Componente custom
├── views.py             # Monte Carlo, Basket, FIRE
├── views2.py            # Real Estate, Rebalance, Tax
├── views3.py            # Ghid investiții
├── logo.png             # Logo aplicație
├── requirements.txt     # Dependențe Python
└── .github/
    └── workflows/
        └── build.yml    # GitHub Actions CI/CD
```

### Build local

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=logo.ico --add-data "logo.png;." main_app.py
```

---

## 📄 Licență

MIT License - vezi [LICENSE](LICENSE)

---

## 👤 Autor

**ManuX**

---

## ⚠️ Disclaimer

Acest software este doar pentru informare și nu constituie sfat financiar. 
Consultă un specialist înainte de a lua decizii de investiție.
