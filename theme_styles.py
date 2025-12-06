"""
ManuX Wealth OS - Partea 1: Teme și Stiluri (VERSIUNE ACTUALIZATĂ)
"""

import customtkinter as ctk
from typing import Literal

# ═══════════════════════════════════════════════════════════════
# 🎨 PALETĂ DE CULORI
# ═══════════════════════════════════════════════════════════════

COLORS_DARK = {
    "page_bg": "#0F172A",
    "panel_bg": "#1E293B",
    "card_bg": "#334155",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
}

COLORS_LIGHT = {
    "page_bg": "#F8FAFC",
    "panel_bg": "#FFFFFF",
    "card_bg": "#E2E8F0",
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
}

COLORS = {
    # Accent Colors (shared)
    "accent": "#3B82F6",
    "accent_hover": "#2563EB",
    "success": "#10B981",
    "success_hover": "#059669",
    "danger": "#EF4444",
    "danger_hover": "#DC2626",
    "warning": "#F59E0B",
    "warning_hover": "#D97706",
    "info": "#06B6D4",
    "purple": "#8B5CF6",
    "purple_hover": "#7C3AED",
    "pink": "#EC4899",
    "pink_hover": "#DB2777",
    "cyan": "#06B6D4",
    "gold": "#FBBF24",
    "emerald": "#34D399",
    "border": "#475569",
    
    # Special backgrounds
    "monte_carlo_bg": "#1E1B4B",
    "monte_carlo_card": "#312E81",
    "fire_bg": "#78350F",
    "fire_card": "#92400E",
    "basket_success_bg": "#064E3B",
    "tax_danger_bg": "#7F1D1D",
    "tax_danger_card": "#991B1B",
    "guide_purple_bg": "#581C87",
    "guide_purple_card": "#6B21A8",
}

FONTS = {
    "primary": ("Segoe UI Variable", 14),
    "primary_bold": ("Segoe UI Variable", 14, "bold"),
    "header": ("Segoe UI Variable", 24, "bold"),
    "subheader": ("Segoe UI Variable", 18, "bold"),
    "section_title": ("Segoe UI Variable", 13, "bold"),
    "body": ("Segoe UI Variable", 14),
    "caption": ("Segoe UI Variable", 12),
    "mono": ("Cascadia Code", 16, "bold"),
    "mono_small": ("Cascadia Code", 14),
    "button": ("Segoe UI Variable", 15, "bold"),
    "small": ("Segoe UI Variable", 11),
}


class ThemeManager:
    """Manager pentru tema aplicației cu suport real pentru schimbare"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._current_theme = "dark"
        self._callbacks = []
        self._widgets = []
    
    @property
    def is_dark(self) -> bool:
        return self._current_theme == "dark"
    
    def get_colors(self):
        return COLORS_DARK if self.is_dark else COLORS_LIGHT
    
    def get(self, key: str) -> str:
        colors = self.get_colors()
        return colors.get(key, COLORS.get(key, "#FFFFFF"))
    
    def register_widget(self, widget, update_func):
        """Înregistrează widget pentru actualizare la schimbarea temei"""
        self._widgets.append((widget, update_func))
    
    def toggle_theme(self):
        self._current_theme = "light" if self.is_dark else "dark"
        ctk.set_appearance_mode(self._current_theme)
        
        # Actualizează toate widget-urile înregistrate
        for widget, update_func in self._widgets[:]:
            try:
                update_func()
            except:
                self._widgets.remove((widget, update_func))
        
        for callback in self._callbacks:
            try:
                callback(self._current_theme)
            except:
                pass
    
    def on_theme_change(self, callback):
        self._callbacks.append(callback)


theme_manager = ThemeManager()


BUTTON_STYLES = {
    "primary": {
        "fg_color": COLORS["accent"],
        "hover_color": COLORS["accent_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "success": {
        "fg_color": COLORS["success"],
        "hover_color": COLORS["success_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "danger": {
        "fg_color": COLORS["danger"],
        "hover_color": COLORS["danger_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "warning": {
        "fg_color": COLORS["warning"],
        "hover_color": COLORS["warning_hover"],
        "text_color": "#1F2937",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "purple": {
        "fg_color": COLORS["purple"],
        "hover_color": COLORS["purple_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "cyan": {
        "fg_color": COLORS["cyan"],
        "hover_color": COLORS["accent_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "pink": {
        "fg_color": COLORS["pink"],
        "hover_color": COLORS["pink_hover"],
        "text_color": "white",
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
    "secondary": {
        "fg_color": COLORS_DARK["card_bg"],
        "hover_color": COLORS["accent"],
        "text_color": COLORS_DARK["text_primary"],
        "corner_radius": 12,
        "height": 48,
        "font": FONTS["primary_bold"],
    },
    "gold": {
        "fg_color": "#1F2937",
        "hover_color": COLORS["gold"],
        "text_color": COLORS["gold"],
        "corner_radius": 14,
        "height": 52,
        "font": FONTS["button"],
    },
}


def create_styled_button(parent, text: str, style_name: str = "primary", 
                         command=None, **kwargs) -> ctk.CTkButton:
    style = BUTTON_STYLES.get(style_name, BUTTON_STYLES["primary"]).copy()
    style.update(kwargs)
    return ctk.CTkButton(parent, text=text, command=command, **style)


def create_styled_entry(parent, placeholder: str = "", **kwargs) -> ctk.CTkEntry:
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        fg_color=COLORS_DARK["card_bg"],
        text_color=COLORS_DARK["text_primary"],
        corner_radius=10,
        height=44,
        font=FONTS["body"],
        **kwargs
    )


def format_currency(value: float, currency: str = "EUR") -> str:
    symbols = {"EUR": "€", "USD": "$", "RON": "lei", "CAD": "C$", "GBP": "£", "CHF": "Fr."}
    symbol = symbols.get(currency, currency)
    formatted = f"{value:,.0f}".replace(",", " ")
    if currency == "RON":
        return f"{formatted} {symbol}"
    return f"{symbol} {formatted}"


def format_percentage(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%"


def init_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
