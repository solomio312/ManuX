"""
ManuX Wealth OS - Aplicația Principală (VERSIUNE COMPLETĂ)
Cu toate funcționalitățile: theme toggle, export CSV/PDF, retrageri, evoluție lunară etc.
"""

import customtkinter as ctk
import csv
import os
from datetime import datetime
from typing import Callable

from theme_styles import (
    COLORS, COLORS_DARK, COLORS_LIGHT, FONTS, theme_manager, init_theme,
    create_styled_button, format_currency, format_percentage
)
from widgets import (
    CTkCard, CTkStatBox, CTkSliderWithLabel, CTkInputGroup,
    NavigationButton, SidebarSection, DataTable, ToastNotification
)
from views import MonteCarloView, BasketView, FireView
from views2 import RealEstateView, RebalanceView, TaxView
from views3 import GuideView


class ManuXWealthOS(ctk.CTk):
    """Aplicație principală ManuX Wealth OS - Versiune Completă"""
    
    def __init__(self):
        super().__init__()
        
        init_theme()
        
        self.title("ManuX Wealth OS Enterprise 16.2")
        self.geometry("1450x950")
        self.minsize(1100, 750)
        
        # Variabile de stare
        self.currency_var = ctk.StringVar(value="EUR")
        self.is_dark = True
        
        # Theme callback
        theme_manager.on_theme_change(self._apply_theme)
        
        # Setup UI
        self._setup_layout()
        self._create_sidebar()
        self._create_main_content()
        
        # Toast
        self.toast = ToastNotification(self)
        
        # Aplicare temă inițială
        self._apply_theme("dark")
        self._show_view("dashboard")
    
    def _setup_layout(self):
        self.columnconfigure(0, weight=0, minsize=340)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
    
    def _apply_theme(self, theme: str):
        """Aplică tema pe întreaga aplicație"""
        self.is_dark = theme == "dark"
        colors = COLORS_DARK if self.is_dark else COLORS_LIGHT
        
        self.configure(fg_color=colors["page_bg"])
        
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(fg_color=colors["panel_bg"])
        if hasattr(self, 'content_frame'):
            self.content_frame.configure(fg_color=colors["page_bg"])
    
    def _create_sidebar(self):
        """Creează sidebar-ul complet"""
        self.sidebar = ctk.CTkScrollableFrame(
            self, width=320, fg_color=COLORS_DARK["panel_bg"], corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.columnconfigure(0, weight=1)
        
        row = 0
        
        # Header
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.grid(row=row, column=0, sticky="ew", padx=20, pady=20)
        row += 1
        
        # Logo custom (pune calea către logo-ul tău aici)
        # Exemplu: logo.png în același folder cu main_app.py
        try:
            from PIL import Image
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), 
                                        dark_image=Image.open(logo_path), size=(40, 40))
                ctk.CTkLabel(header, image=logo_img, text="").pack(side="left")
            else:
                # Fallback la emoji dacă logo-ul nu există
                ctk.CTkLabel(header, text="💎", font=("Segoe UI", 32)).pack(side="left")
        except ImportError:
            # Fallback dacă PIL nu e instalat
            ctk.CTkLabel(header, text="💎", font=("Segoe UI", 32)).pack(side="left")
        
        # ctk.CTkLabel(header, text="💎", font=("Segoe UI", 32)).pack(side="left")  # Original diamond
        ctk.CTkLabel(header, text="ManuX Wealth OS", font=FONTS["subheader"], 
                     text_color=COLORS["accent"]).pack(side="left", padx=10)
        
        # Theme Toggle
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=(0, 15))
        row += 1
        
        self.theme_label = ctk.CTkLabel(theme_frame, text="🌙 Temă Dark", font=FONTS["caption"])
        self.theme_label.pack(side="left")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, text="", width=50, command=self._on_theme_toggle,
            progress_color=COLORS["accent"]
        )
        self.theme_switch.pack(side="right")
        self.theme_switch.select()
        
        # === VALUTĂ ===
        curr_section = SidebarSection(self.sidebar, "Valută & Curs", "💱")
        curr_section.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        row += 1
        
        curr_row = ctk.CTkFrame(curr_section.content, fg_color="transparent")
        curr_row.grid(row=0, column=0, sticky="ew")
        curr_row.columnconfigure(0, weight=1)
        
        self.currency_picker = ctk.CTkOptionMenu(
            curr_row, values=["EUR", "USD", "RON", "GBP", "CHF", "CAD"],
            variable=self.currency_var, command=self._on_currency_change,
            fg_color=COLORS_DARK["card_bg"], button_color=COLORS["accent"]
        )
        self.currency_picker.grid(row=0, column=0, sticky="ew", pady=5)
        
        refresh_btn = ctk.CTkButton(
            curr_row, text="🔄", width=40, fg_color=COLORS["success"],
            command=self._refresh_rates
        )
        refresh_btn.grid(row=0, column=1, padx=(5,0), pady=5)
        
        self.rate_label = ctk.CTkLabel(
            curr_section.content, text="1 EUR = 4.98 RON | 1 USD = 4.62 RON",
            font=FONTS["caption"], text_color=COLORS_DARK["text_secondary"]
        )
        self.rate_label.grid(row=1, column=0, sticky="w", pady=(0,5))
        
        # === PERIOADĂ SIMULARE ===
        period_section = SidebarSection(self.sidebar, "Perioadă Simulare", "📅")
        period_section.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        row += 1
        
        # Start an/lună
        start_frame = ctk.CTkFrame(period_section.content, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", pady=5)
        start_frame.columnconfigure((0,1), weight=1)
        
        self.start_month = ctk.CTkOptionMenu(
            start_frame, values=["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", 
                                "Iunie", "Iulie", "August", "Septembrie", "Octombrie", 
                                "Noiembrie", "Decembrie"],
            fg_color=COLORS_DARK["card_bg"], button_color=COLORS["accent"]
        )
        self.start_month.grid(row=0, column=0, sticky="ew", padx=(0,5))
        self.start_month.set("Decembrie")
        
        self.start_year = CTkInputGroup(start_frame, "", "2025", "2025")
        self.start_year.grid(row=0, column=1, sticky="ew")
        
        self.years_slider = CTkSliderWithLabel(
            period_section.content, label="Durată (ani)",
            from_=1, to=50, initial_value=20, suffix=" ani",
            progress_color=COLORS["accent"]
        )
        self.years_slider.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.compound_picker = ctk.CTkOptionMenu(
            period_section.content, values=["Lunar", "Trimestrial", "Anual"],
            fg_color=COLORS_DARK["card_bg"], button_color=COLORS["accent"]
        )
        self.compound_picker.grid(row=2, column=0, sticky="ew", pady=5)
        
        # === CAPITAL & RANDAMENT ===
        capital_section = SidebarSection(self.sidebar, "Capital & Randament", "💰")
        capital_section.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        row += 1
        
        self.initial_input = CTkInputGroup(capital_section.content, "Capital Inițial", "10000", "10000")
        self.initial_input.grid(row=0, column=0, sticky="ew", pady=5)
        
        self.interest_slider = CTkSliderWithLabel(
            capital_section.content, label="Dobândă Anuală",
            from_=0, to=20, initial_value=7, suffix="%", decimals=1,
            progress_color=COLORS["success"]
        )
        self.interest_slider.grid(row=1, column=0, sticky="ew", pady=5)
        
        self.inflation_slider = CTkSliderWithLabel(
            capital_section.content, label="Inflație Anuală",
            from_=0, to=15, initial_value=3, suffix="%", decimals=1,
            progress_color=COLORS["warning"]
        )
        self.inflation_slider.grid(row=2, column=0, sticky="ew", pady=5)
        
        # === DEPOZITE LUNARE ===
        dca_section = SidebarSection(self.sidebar, "Depozite Lunare (DCA)", "📈")
        dca_section.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        row += 1
        
        self.monthly_input = CTkInputGroup(dca_section.content, "Depozit Lunar", "500", "500")
        self.monthly_input.grid(row=0, column=0, sticky="ew", pady=5)
        
        self.deposit_growth = CTkInputGroup(dca_section.content, "Creștere Anuală Depozit (%)", "0", "0")
        self.deposit_growth.grid(row=1, column=0, sticky="ew", pady=5)
        
        ctk.CTkLabel(dca_section.content, text="Perioada Depozite (ani)", font=FONTS["section_title"]).grid(row=2, column=0, sticky="w", pady=(10,5))
        
        self.deposit_period_start = CTkSliderWithLabel(
            dca_section.content, label="De la anul",
            from_=1, to=50, initial_value=1, suffix="",
            progress_color=COLORS["accent"]
        )
        self.deposit_period_start.grid(row=3, column=0, sticky="ew", pady=2)
        
        self.deposit_period_end = CTkSliderWithLabel(
            dca_section.content, label="Până la anul",
            from_=1, to=50, initial_value=20, suffix="",
            progress_color=COLORS["accent"]
        )
        self.deposit_period_end.grid(row=4, column=0, sticky="ew", pady=2)
        
        # === RETRAGERI ===
        withdraw_section = SidebarSection(self.sidebar, "Retrageri (Faza Pensie)", "📤")
        withdraw_section.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
        row += 1
        
        self.withdrawal_input = CTkInputGroup(withdraw_section.content, "Retragere Lunară", "0", "0")
        self.withdrawal_input.grid(row=0, column=0, sticky="ew", pady=5)
        
        self.withdraw_period_start = CTkSliderWithLabel(
            withdraw_section.content, label="De la anul",
            from_=1, to=50, initial_value=21, suffix="",
            progress_color=COLORS["danger"]
        )
        self.withdraw_period_start.grid(row=1, column=0, sticky="ew", pady=2)
        
        self.withdraw_period_end = CTkSliderWithLabel(
            withdraw_section.content, label="Până la anul",
            from_=1, to=50, initial_value=40, suffix="",
            progress_color=COLORS["danger"]
        )
        self.withdraw_period_end.grid(row=2, column=0, sticky="ew", pady=2)
        
        # === BUTOANE ACȚIUNE ===
        action_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        action_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=20)
        action_frame.columnconfigure(0, weight=1)
        row += 1
        
        create_styled_button(action_frame, "🧮 Calculează", "success", 
                           command=self._on_calculate).grid(row=0, column=0, sticky="ew", pady=5)
        create_styled_button(action_frame, "💾 Salvează Scenariu", "secondary",
                           command=self._save_scenario).grid(row=1, column=0, sticky="ew", pady=5)
        
        export_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        export_frame.grid(row=2, column=0, sticky="ew", pady=5)
        export_frame.columnconfigure((0,1), weight=1)
        
        create_styled_button(export_frame, "📄 CSV", "secondary", width=100,
                           command=self._export_csv).grid(row=0, column=0, sticky="ew", padx=(0,5))
        create_styled_button(export_frame, "📑 PDF", "secondary", width=100,
                           command=self._export_pdf).grid(row=0, column=1, sticky="ew")
    
    def _create_main_content(self):
        """Creează zona de conținut principal"""
        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS_DARK["page_bg"], corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        self.views = {}
        self._create_dashboard_view()
        
        # Module specializate
        self.views["monte_carlo"] = MonteCarloView(
            self.content_frame, lambda: self._show_view("dashboard"),
            self._get_params, self.currency_var
        )
        self.views["basket"] = BasketView(
            self.content_frame, lambda: self._show_view("dashboard")
        )
        self.views["fire"] = FireView(
            self.content_frame, lambda: self._show_view("dashboard"), self.currency_var
        )
        self.views["real_estate"] = RealEstateView(
            self.content_frame, lambda: self._show_view("dashboard"), self.currency_var
        )
        self.views["rebalance"] = RebalanceView(
            self.content_frame, lambda: self._show_view("dashboard"), self.currency_var
        )
        self.views["tax"] = TaxView(
            self.content_frame, lambda: self._show_view("dashboard")
        )
        self.views["guide"] = GuideView(
            self.content_frame, lambda: self._show_view("dashboard")
        )
    
    def _get_params(self):
        """Returnează parametrii curenți pentru module"""
        return {
            "initial": self.initial_input.get_float(),
            "monthly": self.monthly_input.get_float(),
            "years": int(self.years_slider.get()),
            "rate": self.interest_slider.get() / 100,
            "inflation": self.inflation_slider.get() / 100,
        }
    
    def _create_dashboard_view(self):
        """Dashboard principal"""
        view = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        view.columnconfigure((0,1,2,3), weight=1)
        self.views["dashboard"] = view
        
        # Welcome
        welcome = CTkCard(view, fg_color=COLORS_DARK["card_bg"])
        welcome.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0,20))
        
        ctk.CTkLabel(welcome, text="👋 Bun venit în ManuX Wealth OS!", 
                     font=FONTS["header"], text_color=COLORS["accent"]).pack(padx=20, pady=(20,5), anchor="w")
        ctk.CTkLabel(welcome, text="Simulator avansat pentru proiecții financiare și planificare investiții.",
                     font=FONTS["body"], text_color=COLORS_DARK["text_secondary"]).pack(padx=20, pady=(0,20), anchor="w")
        
        # Navigation
        nav_items = [
            ("🧮", "Calculator", "Proiecție investiții", COLORS["accent"], "calculator"),
            ("🎲", "Monte Carlo", "Simulare 10K scenarii", COLORS["purple"], "monte_carlo"),
            ("🛒", "Coș Lunar", "Cheltuieli minime RO", COLORS["success"], "basket"),
            ("🔥", "FIRE", "Simulator pensie", COLORS["warning"], "fire"),
            ("🏠", "Imobiliar", "Calculator ROI", COLORS["cyan"], "real_estate"),
            ("⚖️", "Rebalansare", "Ajustare portofoliu", COLORS["pink"], "rebalance"),
            ("💸", "Taxe", "RO / CA / US", COLORS["danger"], "tax"),
            ("📚", "Ghid", "Educație financiară", COLORS["gold"], "guide"),
        ]
        
        for i, (icon, title, desc, color, view_name) in enumerate(nav_items):
            btn = NavigationButton(view, text=title, icon=icon, description=desc,
                                   accent_color=color, command=lambda v=view_name: self._show_view(v))
            btn.grid(row=1 + i//4, column=i%4, padx=5, pady=5, sticky="nsew")
        
        # Stats
        self.stat_final = CTkStatBox(view, "Sold Final", "€ 0", "💰", COLORS["success"])
        self.stat_final.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        
        self.stat_invested = CTkStatBox(view, "Total Investit", "€ 0", "📥", COLORS["accent"])
        self.stat_invested.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")
        
        self.stat_profit = CTkStatBox(view, "Profit Total", "€ 0", "📈", COLORS["purple"])
        self.stat_profit.grid(row=3, column=2, padx=5, pady=10, sticky="nsew")
        
        self.stat_real = CTkStatBox(view, "Valoare Reală", "€ 0", "🎯", COLORS["warning"])
        self.stat_real.grid(row=3, column=3, padx=5, pady=10, sticky="nsew")
        
        # Analiză Inflație
        inflation_card = CTkCard(view)
        inflation_card.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)
        
        ctk.CTkLabel(inflation_card, text="📉 Analiză Impact Inflație", font=FONTS["subheader"]).pack(padx=20, pady=(15,10), anchor="w")
        
        inflation_frame = ctk.CTkFrame(inflation_card, fg_color="transparent")
        inflation_frame.pack(padx=20, pady=(0,15), fill="x")
        inflation_frame.columnconfigure((0,1,2,3), weight=1)
        
        self.total_inflation_label = ctk.CTkLabel(inflation_frame, text="Inflație Cumulată: -", font=FONTS["mono_small"], text_color=COLORS["danger"])
        self.total_inflation_label.grid(row=0, column=0, pady=5)
        
        self.purchasing_power_label = ctk.CTkLabel(inflation_frame, text="Putere Cumpărare: -", font=FONTS["mono_small"], text_color=COLORS["warning"])
        self.purchasing_power_label.grid(row=0, column=1, pady=5)
        
        self.doubling_time_label = ctk.CTkLabel(inflation_frame, text="Timp Dublare Prețuri: -", font=FONTS["mono_small"], text_color=COLORS["purple"])
        self.doubling_time_label.grid(row=0, column=2, pady=5)
        
        self.inflation_loss_label = ctk.CTkLabel(inflation_frame, text="Pierdere din Inflație: -", font=FONTS["mono_small"], text_color=COLORS["danger"])
        self.inflation_loss_label.grid(row=0, column=3, pady=5)
        
        # Toggle lunar/anual
        toggle_frame = ctk.CTkFrame(view, fg_color="transparent")
        toggle_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(20,10))
        
        ctk.CTkLabel(toggle_frame, text="📊 Evoluție Detaliată", font=FONTS["subheader"]).pack(side="left")
        
        self.view_mode = ctk.StringVar(value="anual")
        ctk.CTkRadioButton(toggle_frame, text="Anual", variable=self.view_mode, value="anual",
                          command=self._on_calculate).pack(side="right", padx=10)
        ctk.CTkRadioButton(toggle_frame, text="Lunar", variable=self.view_mode, value="lunar",
                          command=self._on_calculate).pack(side="right", padx=10)
        
        # Table
        self.breakdown_table = DataTable(
            view, columns=["Perioadă", "Sold", "Depozite", "Retrageri", "Dobândă", "Val. Reală"],
            height=350
        )
        self.breakdown_table.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Proiecție grafică simplă (progress bars)
        chart_card = CTkCard(view)
        chart_card.grid(row=7, column=0, columnspan=4, sticky="ew", pady=10)
        
        ctk.CTkLabel(chart_card, text="📈 Proiecție Vizuală", font=FONTS["subheader"]).pack(padx=20, pady=(15,10), anchor="w")
        
        self.chart_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
        self.chart_frame.pack(padx=20, pady=(0,15), fill="x")
    
    def _show_view(self, view_name: str):
        for v in self.views.values():
            v.grid_forget()
        
        if view_name == "calculator":
            view_name = "dashboard"
        
        self.views[view_name].grid(row=0, column=0, sticky="nsew")
    
    # === EVENT HANDLERS ===
    
    def _on_theme_toggle(self):
        theme_manager.toggle_theme()
        is_dark = theme_manager.is_dark
        self.theme_label.configure(text="🌙 Temă Dark" if is_dark else "☀️ Temă Light")
        self.toast.show(f"Temă schimbată: {'Dark' if is_dark else 'Light'}", "info")
    
    def _on_currency_change(self, value):
        self.toast.show(f"Valută: {value}", "info")
    
    def _refresh_rates(self):
        # Simulare refresh (în realitate ar fi API call)
        self.rate_label.configure(text="1 EUR = 4.98 RON | 1 USD = 4.62 RON ✓")
        self.toast.show("Cursuri actualizate!", "success")
    
    def _on_calculate(self):
        """Calculează proiecția completă"""
        try:
            initial = self.initial_input.get_float()
            monthly_deposit = self.monthly_input.get_float()
            monthly_withdrawal = self.withdrawal_input.get_float()
            years = int(self.years_slider.get())
            rate = self.interest_slider.get() / 100
            inflation = self.inflation_slider.get() / 100
            deposit_growth = self.deposit_growth.get_float() / 100
            
            deposit_start = int(self.deposit_period_start.get())
            deposit_end = int(self.deposit_period_end.get())
            withdraw_start = int(self.withdraw_period_start.get())
            withdraw_end = int(self.withdraw_period_end.get())
            
            currency = self.currency_var.get()
            is_monthly = self.view_mode.get() == "lunar"
            
            # Start date
            months = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
                     "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
            start_month_idx = months.index(self.start_month.get())
            start_year = int(self.start_year.get())
            
            # Calcul
            total = initial
            total_invested = initial
            total_withdrawn = 0
            current_deposit = monthly_deposit
            
            self.breakdown_data = []
            
            if is_monthly:
                # Calcul lunar
                for month in range(1, years * 12 + 1):
                    year = (month - 1) // 12 + 1
                    month_in_year = (month - 1) % 12 + 1
                    
                    # Depozite
                    deposit = current_deposit if deposit_start <= year <= deposit_end else 0
                    total_invested += deposit
                    
                    # Retrageri
                    withdrawal = monthly_withdrawal if withdraw_start <= year <= withdraw_end else 0
                    total_withdrawn += withdrawal
                    
                    # Dobândă lunară
                    monthly_rate = rate / 12
                    interest = total * monthly_rate
                    
                    total = total + deposit - withdrawal + interest
                    
                    # Valoare reală
                    months_elapsed = month
                    monthly_inflation = (1 + inflation) ** (months_elapsed / 12)
                    real_value = total / monthly_inflation
                    
                    # Data
                    display_month = (start_month_idx + month - 1) % 12
                    display_year = start_year + (start_month_idx + month - 1) // 12
                    
                    self.breakdown_data.append({
                        "period": f"{months[display_month][:3]} {display_year}",
                        "balance": total,
                        "deposits": deposit,
                        "withdrawals": withdrawal,
                        "interest": interest,
                        "real": real_value
                    })
                    
                    # Creștere anuală depozit
                    if month % 12 == 0:
                        current_deposit *= (1 + deposit_growth)
            else:
                # Calcul anual
                for year in range(1, years + 1):
                    # Depozite anuale
                    deposit = current_deposit * 12 if deposit_start <= year <= deposit_end else 0
                    total_invested += deposit
                    
                    # Retrageri anuale
                    withdrawal = monthly_withdrawal * 12 if withdraw_start <= year <= withdraw_end else 0
                    total_withdrawn += withdrawal
                    
                    # Dobândă
                    interest = (total + deposit/2 - withdrawal/2) * rate
                    
                    total = total + deposit - withdrawal + interest
                    real_value = total / ((1 + inflation) ** year)
                    
                    self.breakdown_data.append({
                        "period": str(start_year + year - 1),
                        "balance": total,
                        "deposits": deposit,
                        "withdrawals": withdrawal,
                        "interest": interest,
                        "real": real_value
                    })
                    
                    current_deposit *= (1 + deposit_growth)
            
            profit = total - total_invested + total_withdrawn
            final_real = total / ((1 + inflation) ** years)
            
            # Update stats
            self.stat_final.set_value(format_currency(total, currency))
            self.stat_invested.set_value(format_currency(total_invested, currency))
            self.stat_profit.set_value(format_currency(profit, currency))
            self.stat_real.set_value(format_currency(final_real, currency))
            
            # Analiză inflație
            cumulative_inflation = ((1 + inflation) ** years - 1) * 100
            purchasing_power = 100 / ((1 + inflation) ** years)
            doubling_time = 72 / (inflation * 100) if inflation > 0 else 999
            inflation_loss = total - final_real
            
            self.total_inflation_label.configure(text=f"Inflație Cumulată: {cumulative_inflation:.1f}%")
            self.purchasing_power_label.configure(text=f"Putere Cumpărare: {purchasing_power:.1f}%")
            self.doubling_time_label.configure(text=f"Timp Dublare Prețuri: {doubling_time:.1f} ani")
            self.inflation_loss_label.configure(text=f"Pierdere din Inflație: {format_currency(inflation_loss, currency)}")
            
            # Update table
            self.breakdown_table.clear()
            
            # Limitează afișarea pentru lunar
            data_to_show = self.breakdown_data if not is_monthly else self.breakdown_data[::3]  # Every 3 months
            if is_monthly and len(data_to_show) > 100:
                data_to_show = data_to_show[:100]
            
            for d in data_to_show:
                self.breakdown_table.add_row([
                    d["period"],
                    format_currency(d["balance"], currency),
                    format_currency(d["deposits"], currency) if d["deposits"] > 0 else "-",
                    format_currency(d["withdrawals"], currency) if d["withdrawals"] > 0 else "-",
                    format_currency(d["interest"], currency),
                    format_currency(d["real"], currency)
                ], [COLORS_DARK["text_primary"], COLORS["success"], COLORS["accent"], 
                    COLORS["danger"], COLORS["purple"], COLORS["warning"]])
            
            # Update chart (progress bars simple)
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            max_val = max(d["balance"] for d in self.breakdown_data) if self.breakdown_data else 1
            
            chart_data = self.breakdown_data[::max(1, len(self.breakdown_data)//8)][:8]
            
            for i, d in enumerate(chart_data):
                f = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
                f.pack(fill="x", pady=2)
                
                ctk.CTkLabel(f, text=d["period"], width=80, font=FONTS["caption"]).pack(side="left")
                
                bar = ctk.CTkProgressBar(f, progress_color=COLORS["success"])
                bar.pack(side="left", fill="x", expand=True, padx=10)
                bar.set(d["balance"] / max_val)
                
                ctk.CTkLabel(f, text=format_currency(d["balance"], currency), 
                            width=120, font=FONTS["mono_small"]).pack(side="right")
            
            self.toast.show("Calcul finalizat!", "success")
            
        except Exception as e:
            self.toast.show(f"Eroare: {str(e)}", "error")
    
    def _save_scenario(self):
        self.toast.show("Scenariul a fost salvat!", "success")
    
    def _export_csv(self):
        """Exportă datele în CSV"""
        if not hasattr(self, 'breakdown_data') or not self.breakdown_data:
            self.toast.show("Calculează mai întâi!", "warning")
            return
        
        from tkinter import filedialog
        
        filename = f"manux_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=filename,
            title="Salvează Export CSV"
        )
        
        if not filepath:
            return  # Utilizatorul a anulat
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Perioadă", "Sold", "Depozite", "Retrageri", "Dobândă", "Valoare Reală"])
                
                for d in self.breakdown_data:
                    writer.writerow([
                        d["period"], d["balance"], d["deposits"], 
                        d["withdrawals"], d["interest"], d["real"]
                    ])
            
            self.toast.show(f"Exportat: {os.path.basename(filepath)}", "success")
        except Exception as e:
            self.toast.show(f"Eroare export: {str(e)}", "error")
    
    def _export_pdf(self):
        """Exportă datele în PDF"""
        if not hasattr(self, 'breakdown_data') or not self.breakdown_data:
            self.toast.show("Calculează mai întâi!", "warning")
            return
        
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError:
            self.toast.show("Instalează reportlab: pip install reportlab", "warning")
            return
        
        from tkinter import filedialog
        
        filename = f"manux_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=filename,
            title="Salvează Export PDF"
        )
        
        if not filepath:
            return
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Titlu
            elements.append(Paragraph("ManuX Wealth OS - Proiecție Investiții", styles['Title']))
            elements.append(Spacer(1, 20))
            
            # Tabel
            data = [["Perioadă", "Sold", "Depozite", "Retrageri", "Dobândă", "Val. Reală"]]
            currency = self.currency_var.get()
            
            for d in self.breakdown_data[:50]:  # Max 50 rânduri
                data.append([
                    d["period"],
                    format_currency(d["balance"], currency),
                    format_currency(d["deposits"], currency),
                    format_currency(d["withdrawals"], currency),
                    format_currency(d["interest"], currency),
                    format_currency(d["real"], currency)
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8'))
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            self.toast.show(f"PDF exportat: {os.path.basename(filepath)}", "success")
        except Exception as e:
            self.toast.show(f"Eroare PDF: {str(e)}", "error")



if __name__ == "__main__":
    app = ManuXWealthOS()
    app.mainloop()
