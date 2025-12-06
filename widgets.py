"""
ManuX Wealth OS - Partea 2: Widget-uri Custom
Conversie din XAML/.NET MAUI în Python/CustomTkinter

Componente reutilizabile:
- CTkCard, CTkStatBox, CTkSliderWithLabel
- CTkInputGroup, NavigationButton
- SidebarSection, ProgressIndicator
"""

import customtkinter as ctk
from typing import Callable, Optional, Literal
from theme_styles import (
    COLORS, COLORS_DARK, FONTS, BUTTON_STYLES,
    theme_manager, format_currency, format_percentage
)



# ═══════════════════════════════════════════════════════════════
# 📦 CTkCard - Card cu fundal și border radius
# ═══════════════════════════════════════════════════════════════

class CTkCard(ctk.CTkFrame):
    """Card stilizat cu fundal și corner radius"""
    
    def __init__(self, parent, 
                 fg_color: str = None,
                 corner_radius: int = 16,
                 border_width: int = 0,
                 border_color: str = None,
                 **kwargs):
        
        super().__init__(
            parent,
            fg_color=fg_color or COLORS_DARK["card_bg"],
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=border_color or COLORS["border"],
            **kwargs
        )


# ═══════════════════════════════════════════════════════════════
# 📊 CTkStatBox - Box pentru statistici (sold, profit, etc.)
# ═══════════════════════════════════════════════════════════════

class CTkStatBox(CTkCard):
    """Box pentru afișarea statisticilor cu titlu, valoare și icon"""
    
    def __init__(self, parent,
                 title: str,
                 value: str = "0",
                 icon: str = "💰",
                 accent_color: str = None,
                 **kwargs):
        
        super().__init__(parent, **kwargs)
        
        self._accent_color = accent_color or COLORS["accent"]
        
        # Container interior
        self.columnconfigure(0, weight=1)
        
        # Header cu icon și titlu
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))
        
        self.icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=FONTS["subheader"],
        )
        self.icon_label.pack(side="left", padx=(0, 8))
        
        self.title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=FONTS["caption"],
            text_color=COLORS_DARK["text_secondary"]
        )
        self.title_label.pack(side="left")
        
        # Valoare
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=FONTS["mono"],
            text_color=self._accent_color
        )
        self.value_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))
    
    def set_value(self, value: str):
        """Actualizează valoarea afișată"""
        self.value_label.configure(text=value)
    
    def set_accent(self, color: str):
        """Schimbă culoarea accent"""
        self._accent_color = color
        self.value_label.configure(text_color=color)


# ═══════════════════════════════════════════════════════════════
# 🎚️ CTkSliderWithLabel - Slider cu label dinamic
# ═══════════════════════════════════════════════════════════════

class CTkSliderWithLabel(ctk.CTkFrame):
    """Slider cu label care se actualizează dinamic"""
    
    def __init__(self, parent,
                 label: str,
                 from_: float = 0,
                 to: float = 100,
                 initial_value: float = None,
                 suffix: str = "",
                 decimals: int = 0,
                 progress_color: str = None,
                 command: Callable = None,
                 **kwargs):
        
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._suffix = suffix
        self._decimals = decimals
        self._command = command
        
        self.columnconfigure(0, weight=1)
        
        # Header cu label și valoare
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(
            header,
            text=label,
            font=FONTS["section_title"],
            text_color=COLORS_DARK["text_primary"]
        )
        self.label.grid(row=0, column=0, sticky="w")
        
        self.value_label = ctk.CTkLabel(
            header,
            text="",
            font=FONTS["primary_bold"],
            text_color=progress_color or COLORS["accent"]
        )
        self.value_label.grid(row=0, column=1, sticky="e")
        
        # Slider
        self.slider = ctk.CTkSlider(
            self,
            from_=from_,
            to=to,
            number_of_steps=int((to - from_) * (10 ** decimals)),
            progress_color=progress_color or COLORS["accent"],
            button_color=progress_color or COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            command=self._on_change
        )
        self.slider.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        
        # Set valoare inițială
        if initial_value is not None:
            self.slider.set(initial_value)
        self._update_value_label(self.slider.get())
    
    def _on_change(self, value):
        """Handler intern pentru schimbarea valorii"""
        self._update_value_label(value)
        if self._command:
            self._command(value)
    
    def _update_value_label(self, value):
        """Actualizează label-ul cu valoarea curentă"""
        if self._decimals == 0:
            formatted = f"{int(value)}{self._suffix}"
        else:
            formatted = f"{value:.{self._decimals}f}{self._suffix}"
        self.value_label.configure(text=formatted)
    
    def get(self) -> float:
        """Returnează valoarea curentă"""
        return self.slider.get()
    
    def set(self, value: float):
        """Setează valoarea"""
        self.slider.set(value)
        self._update_value_label(value)


# ═══════════════════════════════════════════════════════════════
# 📝 CTkInputGroup - Label + Entry grupate
# ═══════════════════════════════════════════════════════════════

class CTkInputGroup(ctk.CTkFrame):
    """Grup de label și entry"""
    
    def __init__(self, parent,
                 label: str,
                 placeholder: str = "",
                 default_value: str = "",
                 input_type: Literal["text", "number", "currency"] = "text",
                 **kwargs):
        
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._input_type = input_type
        self.columnconfigure(0, weight=1)
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=FONTS["section_title"],
            text_color=COLORS_DARK["text_primary"],
            anchor="w"
        )
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        # Entry
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            fg_color=COLORS_DARK["card_bg"],
            text_color=COLORS_DARK["text_primary"],
            corner_radius=10,
            height=44,
            font=FONTS["body"]
        )
        self.entry.grid(row=1, column=0, sticky="ew")
        
        if default_value:
            self.entry.insert(0, default_value)
    
    def get(self) -> str:
        """Returnează valoarea din entry"""
        return self.entry.get()
    
    def get_float(self) -> float:
        """Returnează valoarea ca float"""
        try:
            value = self.entry.get().replace(",", ".").replace(" ", "")
            return float(value)
        except ValueError:
            return 0.0
    
    def set(self, value: str):
        """Setează valoarea"""
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


# ═══════════════════════════════════════════════════════════════
# 🧭 NavigationButton - Buton de navigare cu icon
# ═══════════════════════════════════════════════════════════════

class NavigationButton(ctk.CTkButton):
    """Buton de navigare cu icon și text (stil card)"""
    
    def __init__(self, parent,
                 text: str,
                 icon: str = "📊",
                 description: str = "",
                 accent_color: str = None,
                 command: Callable = None,
                 **kwargs):
        
        accent = accent_color or COLORS["accent"]
        
        # Combine icon și text
        display_text = f"{icon}\n{text}"
        if description:
            display_text += f"\n{description}"
        
        super().__init__(
            parent,
            text=display_text,
            font=FONTS["primary_bold"],
            fg_color=COLORS_DARK["card_bg"],
            hover_color=accent,
            text_color=COLORS_DARK["text_primary"],
            corner_radius=16,
            height=100,
            command=command,
            **kwargs
        )
        
        self._accent_color = accent
        
        # Bind hover effects
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
    
    def _on_hover_enter(self, event):
        self.configure(text_color="white")
    
    def _on_hover_leave(self, event):
        self.configure(text_color=COLORS_DARK["text_primary"])


# ═══════════════════════════════════════════════════════════════
# 📁 SidebarSection - Secțiune în sidebar
# ═══════════════════════════════════════════════════════════════

class SidebarSection(ctk.CTkFrame):
    """Secțiune stilizată pentru sidebar"""
    
    def __init__(self, parent,
                 title: str,
                 icon: str = "⚙️",
                 **kwargs):
        
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        
        ctk.CTkLabel(
            header,
            text=icon,
            font=FONTS["body"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=title.upper(),
            font=FONTS["section_title"],
            text_color=COLORS_DARK["text_secondary"]
        ).pack(side="left", padx=(8, 0))
        
        # Content frame
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="ew")
        self.content.columnconfigure(0, weight=1)


# ═══════════════════════════════════════════════════════════════
# ⏳ ProgressIndicator - Indicator de progres circular
# ═══════════════════════════════════════════════════════════════

class ProgressIndicator(ctk.CTkFrame):
    """Indicator de progres cu text"""
    
    def __init__(self, parent,
                 text: str = "Se procesează...",
                 **kwargs):
        
        super().__init__(
            parent, 
            fg_color=COLORS_DARK["card_bg"],
            corner_radius=12,
            **kwargs
        )
        
        self.columnconfigure(0, weight=1)
        
        # Spinner (folosim progressbar indeterminate ca alternativă)
        self.progress = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            progress_color=COLORS["accent"]
        )
        self.progress.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=FONTS["caption"],
            text_color=COLORS_DARK["text_secondary"]
        )
        self.label.grid(row=1, column=0, pady=(0, 20))
    
    def start(self):
        """Pornește animația"""
        self.progress.start()
    
    def stop(self):
        """Oprește animația"""
        self.progress.stop()
    
    def set_text(self, text: str):
        """Actualizează textul"""
        self.label.configure(text=text)


# ═══════════════════════════════════════════════════════════════
# 📋 DataTable - Tabel simplu pentru date
# ═══════════════════════════════════════════════════════════════

class DataTable(ctk.CTkScrollableFrame):
    """Tabel scrollable pentru afișarea datelor"""
    
    def __init__(self, parent, 
                 columns: list[str],
                 **kwargs):
        
        super().__init__(
            parent,
            fg_color=COLORS_DARK["card_bg"],
            corner_radius=12,
            **kwargs
        )
        
        self._columns = columns
        self._rows = []
        
        # Setup grid columns
        for i in range(len(columns)):
            self.columnconfigure(i, weight=1)
        
        # Header row
        for i, col in enumerate(columns):
            header = ctk.CTkLabel(
                self,
                text=col,
                font=FONTS["section_title"],
                text_color=COLORS_DARK["text_secondary"]
            )
            header.grid(row=0, column=i, padx=8, pady=8, sticky="w")
    
    def add_row(self, values: list[str], colors: list[str] = None):
        """Adaugă un rând în tabel"""
        row_idx = len(self._rows) + 1
        self._rows.append(values)
        
        for i, val in enumerate(values):
            color = colors[i] if colors and i < len(colors) else COLORS_DARK["text_primary"]
            
            cell = ctk.CTkLabel(
                self,
                text=val,
                font=FONTS["mono_small"],
                text_color=color
            )
            cell.grid(row=row_idx, column=i, padx=8, pady=4, sticky="w")
    
    def clear(self):
        """Șterge toate rândurile"""
        for widget in self.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()
        self._rows = []


# ═══════════════════════════════════════════════════════════════
# 🔔 ToastNotification - Notificări popup
# ═══════════════════════════════════════════════════════════════

class ToastNotification:
    """Sistem de notificări toast"""
    
    def __init__(self, parent):
        self.parent = parent
        self._toast = None
    
    def show(self, message: str, 
             type_: Literal["success", "error", "warning", "info"] = "info",
             duration: int = 3000):
        """Afișează o notificare toast"""
        
        # Închide toast-ul anterior dacă există
        if self._toast:
            self._toast.destroy()
        
        colors = {
            "success": COLORS["success"],
            "error": COLORS["danger"],
            "warning": COLORS["warning"],
            "info": COLORS["accent"]
        }
        
        icons = {
            "success": "✓",
            "error": "✕",
            "warning": "⚠",
            "info": "ℹ"
        }
        
        self._toast = ctk.CTkFrame(
            self.parent,
            fg_color=colors.get(type_, COLORS["accent"]),
            corner_radius=12
        )
        
        icon_label = ctk.CTkLabel(
            self._toast,
            text=icons.get(type_, "ℹ"),
            font=FONTS["subheader"],
            text_color="white"
        )
        icon_label.pack(side="left", padx=(16, 8), pady=12)
        
        msg_label = ctk.CTkLabel(
            self._toast,
            text=message,
            font=FONTS["body"],
            text_color="white"
        )
        msg_label.pack(side="left", padx=(0, 16), pady=12)
        
        # Poziționare în dreapta jos
        self._toast.place(relx=0.98, rely=0.98, anchor="se")
        
        # Auto-hide după duration ms
        self.parent.after(duration, self._hide_toast)
    
    def _hide_toast(self):
        if self._toast:
            self._toast.destroy()
            self._toast = None


# ═══════════════════════════════════════════════════════════════
# 🏷️ TagBadge - Badge/tag pentru categorii
# ═══════════════════════════════════════════════════════════════

class TagBadge(ctk.CTkFrame):
    """Badge pentru afișarea tag-urilor/categoriilor"""
    
    def __init__(self, parent,
                 text: str,
                 color: str = None,
                 **kwargs):
        
        super().__init__(
            parent,
            fg_color=color or COLORS["accent"],
            corner_radius=8,
            **kwargs
        )
        
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=FONTS["tiny"],
            text_color="white"
        )
        self.label.pack(padx=10, pady=4)


# ═══════════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from theme_styles import init_theme
    
    init_theme()
    
    root = ctk.CTk()
    root.title("Widgets Test")
    root.geometry("800x600")
    root.configure(fg_color=COLORS_DARK["page_bg"])
    
    # Test CTkStatBox
    stat = CTkStatBox(root, title="Sold Final", value="€ 125,430", icon="💰")
    stat.pack(pady=10, padx=20, fill="x")
    
    # Test SliderWithLabel
    slider = CTkSliderWithLabel(
        root, 
        label="Dobândă Anuală",
        from_=0, to=20,
        initial_value=7,
        suffix="%",
        decimals=1,
        progress_color=COLORS["success"]
    )
    slider.pack(pady=10, padx=20, fill="x")
    
    # Test InputGroup
    input_grp = CTkInputGroup(root, label="Capital Inițial", placeholder="10000")
    input_grp.pack(pady=10, padx=20, fill="x")
    
    # Test NavigationButton
    nav_btn = NavigationButton(
        root, 
        text="Calculator",
        icon="🧮",
        description="Proiecție investiții",
        accent_color=COLORS["accent"]
    )
    nav_btn.pack(pady=10, padx=20)
    
    # Test Toast
    toast = ToastNotification(root)
    test_btn = ctk.CTkButton(
        root, 
        text="Show Toast",
        command=lambda: toast.show("Operație reușită!", "success")
    )
    test_btn.pack(pady=10)
    
    root.mainloop()
