"""
ManuX Wealth OS - Module Views (Monte Carlo, Basket, FIRE, etc.)
"""

import customtkinter as ctk
import random
import csv
import os
from datetime import datetime
from typing import Callable

from theme_styles import COLORS, COLORS_DARK, FONTS, theme_manager, format_currency, format_percentage, create_styled_button
from widgets import CTkCard, CTkStatBox, CTkSliderWithLabel, CTkInputGroup, DataTable


# ═══════════════════════════════════════════════════════════════
# 🎲 MONTE CARLO VIEW
# ═══════════════════════════════════════════════════════════════

class MonteCarloView(ctk.CTkScrollableFrame):
    """Simulare Monte Carlo completă"""
    
    def __init__(self, parent, back_command: Callable, get_params: Callable, currency_var):
        super().__init__(parent, fg_color=COLORS["monte_carlo_bg"])
        self.back_command = back_command
        self.get_params = get_params
        self.currency_var = currency_var
        self.columnconfigure((0,1), weight=1)
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(
            header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
            hover_color=COLORS["accent"], command=self.back_command
        ).pack(side="left")
        ctk.CTkLabel(header, text="🎲 Simulare Monte Carlo", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Explicație
        explain = CTkCard(self, fg_color=COLORS["monte_carlo_card"])
        explain.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(explain, text="Ce este simularea Monte Carlo?", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        explanation = """Simularea Monte Carlo rulează mii de scenarii posibile pentru investițiile tale, 
luând în calcul volatilitatea pieței. Rezultatele arată:

• P10 (Pesimist): 10% dintre scenarii au rezultat mai rău
• P50 (Median): Rezultatul mediu - 50% au fost mai bine/rău  
• P90 (Optimist): Doar 10% dintre scenarii au rezultat mai bine

Această analiză îți oferă o imagine realistă a intervalului posibil de rezultate."""
        
        ctk.CTkLabel(explain, text=explanation, font=FONTS["body"], 
                     text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left"
        ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Parametri
        params = CTkCard(self, fg_color=COLORS["monte_carlo_card"])
        params.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(params, text="⚙️ Parametri Simulare", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.volatility = CTkSliderWithLabel(
            params, label="Volatilitate Anuală (%)", from_=5, to=40,
            initial_value=15, suffix="%", progress_color=COLORS["purple"]
        )
        self.volatility.pack(padx=20, pady=5, fill="x")
        
        self.simulations = CTkSliderWithLabel(
            params, label="Număr Simulări", from_=100, to=10000,
            initial_value=1000, suffix="", progress_color=COLORS["cyan"]
        )
        self.simulations.pack(padx=20, pady=5, fill="x")
        
        self.expected_return = CTkInputGroup(params, "Randament Așteptat (%)", "7", "7")
        self.expected_return.pack(padx=20, pady=5, fill="x")
        
        self.mc_inflation = CTkInputGroup(params, "Inflație Estimată (%)", "3", "3")
        self.mc_inflation.pack(padx=20, pady=5, fill="x")
        
        run_btn = create_styled_button(params, "▶️ Rulează Simulare Monte Carlo", "purple", command=self._run)
        run_btn.pack(padx=20, pady=20, fill="x")
        
        # Progres
        self.progress_frame = CTkCard(self, fg_color=COLORS["monte_carlo_card"])
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        self.progress_frame.grid_remove()
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=COLORS["purple"])
        self.progress_bar.pack(padx=20, pady=20, fill="x")
        
        # Rezultate principale
        self.p10 = CTkStatBox(self, "P10 (Pesimist)", "€ 0", "📉", COLORS["danger"])
        self.p10.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        
        self.p50 = CTkStatBox(self, "P50 (Median)", "€ 0", "📊", COLORS["accent"])
        self.p50.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        
        self.p90 = CTkStatBox(self, "P90 (Optimist)", "€ 0", "📈", COLORS["success"])
        self.p90.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        
        self.mean = CTkStatBox(self, "Media (μ)", "€ 0", "μ", COLORS["purple"])
        self.mean.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
        
        # Statistici adiționale
        stats_card = CTkCard(self, fg_color=COLORS["monte_carlo_card"])
        stats_card.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(stats_card, text="📊 Statistici Detaliate", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.stats_frame = ctk.CTkFrame(stats_card, fg_color="transparent")
        self.stats_frame.pack(padx=20, pady=(0,20), fill="x")
        self.stats_frame.columnconfigure((0,1,2,3), weight=1)
        
        self.std_label = ctk.CTkLabel(self.stats_frame, text="Std Dev: -", font=FONTS["mono_small"])
        self.std_label.grid(row=0, column=0, pady=5)
        
        self.min_label = ctk.CTkLabel(self.stats_frame, text="Min: -", font=FONTS["mono_small"])
        self.min_label.grid(row=0, column=1, pady=5)
        
        self.max_label = ctk.CTkLabel(self.stats_frame, text="Max: -", font=FONTS["mono_small"])
        self.max_label.grid(row=0, column=2, pady=5)
        
        self.success_label = ctk.CTkLabel(self.stats_frame, text="Succes: -", font=FONTS["mono_small"], text_color=COLORS["success"])
        self.success_label.grid(row=0, column=3, pady=5)
        
        # Percentile Table
        percentile_card = CTkCard(self, fg_color=COLORS["monte_carlo_card"])
        percentile_card.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(percentile_card, text="📈 Tabel Percentile", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.percentile_table = DataTable(percentile_card, columns=["Percentil", "Valoare", "vs Investit"], height=200)
        self.percentile_table.pack(padx=20, pady=(0,20), fill="x")
    
    def _run(self):
        """Rulează simularea Monte Carlo"""
        params = self.get_params()
        initial = params["initial"]
        monthly = params["monthly"]
        years = params["years"]
        
        rate = self.expected_return.get_float() / 100
        volatility = self.volatility.get() / 100
        n_sims = int(self.simulations.get())
        inflation = self.mc_inflation.get_float() / 100
        
        total_invested = initial + monthly * 12 * years
        
        self.progress_frame.grid()
        self.progress_bar.set(0)
        self.update()
        
        results = []
        for i in range(n_sims):
            total = initial
            for year in range(years):
                yearly_return = random.gauss(rate, volatility)
                total = total * (1 + yearly_return) + monthly * 12
            results.append(total)
            
            if i % 100 == 0:
                self.progress_bar.set(i / n_sims)
                self.update()
        
        self.progress_bar.set(1)
        self.progress_frame.grid_remove()
        
        results.sort()
        currency = self.currency_var.get()
        
        p10 = results[int(n_sims * 0.1)]
        p25 = results[int(n_sims * 0.25)]
        p50 = results[int(n_sims * 0.5)]
        p75 = results[int(n_sims * 0.75)]
        p90 = results[int(n_sims * 0.9)]
        mean_val = sum(results) / n_sims
        std_dev = (sum((x - mean_val) ** 2 for x in results) / n_sims) ** 0.5
        
        self.p10.set_value(format_currency(p10, currency))
        self.p50.set_value(format_currency(p50, currency))
        self.p90.set_value(format_currency(p90, currency))
        self.mean.set_value(format_currency(mean_val, currency))
        
        self.std_label.configure(text=f"Std Dev: {format_currency(std_dev, currency)}")
        self.min_label.configure(text=f"Min: {format_currency(min(results), currency)}")
        self.max_label.configure(text=f"Max: {format_currency(max(results), currency)}")
        
        success_rate = sum(1 for r in results if r > total_invested) / n_sims * 100
        self.success_label.configure(text=f"Succes: {success_rate:.1f}%")
        
        # Percentile table
        self.percentile_table.clear()
        for pct, val in [(10, p10), (25, p25), (50, p50), (75, p75), (90, p90)]:
            vs_invested = ((val / total_invested) - 1) * 100
            color = COLORS["success"] if vs_invested > 0 else COLORS["danger"]
            self.percentile_table.add_row(
                [f"P{pct}", format_currency(val, currency), f"{vs_invested:+.1f}%"],
                [COLORS_DARK["text_primary"], COLORS["accent"], color]
            )


# ═══════════════════════════════════════════════════════════════
# 🛒 BASKET VIEW - Coș Lunar România
# ═══════════════════════════════════════════════════════════════

class BasketView(ctk.CTkScrollableFrame):
    """Coș minim lunar România complet"""
    
    BASKET_DATA = {
        2024: {
            "1 Adult": (2847, "Coșul minim pentru o persoană singură"),
            "2 Adulți": (4523, "Coșul minim pentru un cuplu fără copii"),
            "2 Adulți + 1 Copil": (5891, "Familie cu un copil"),
            "2 Adulți + 2 Copii": (7156, "Familie cu doi copii"),
        },
        2025: {
            "1 Adult": (3102, "Estimare cu inflație 9%"),
            "2 Adulți": (4930, "Estimare cu inflație 9%"),
            "2 Adulți + 1 Copil": (6421, "Estimare cu inflație 9%"),
            "2 Adulți + 2 Copii": (7800, "Estimare cu inflație 9%"),
        }
    }
    
    EUR_RATE = 4.98
    
    def __init__(self, parent, back_command: Callable):
        super().__init__(parent, fg_color="transparent")
        self.back_command = back_command
        self.columnconfigure((0,1), weight=1)
        self.selected_year = 2024
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="🛒 Coș Minim Lunar România", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Explicație
        explain = CTkCard(self, fg_color=COLORS["basket_success_bg"])
        explain.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(explain, text="Ce este Coșul Minim de Consum?", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        explanation = """Coșul minim de consum reprezintă cheltuielile lunare necesare pentru un trai decent, 
calculat de Institutul Național de Statistică (INS). Include:

• Alimente și băuturi non-alcoolice
• Îmbrăcăminte și încălțăminte  
• Locuință, apă, electricitate, gaze
• Transport
• Comunicații
• Sănătate, educație, recreere"""
        
        ctk.CTkLabel(explain, text=explanation, font=FONTS["body"], 
                     text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left"
        ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Selectoare
        select_frame = ctk.CTkFrame(self, fg_color="transparent")
        select_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(select_frame, text="Tip Gospodărie:", font=FONTS["section_title"]).pack(side="left", padx=10)
        
        self.family_picker = ctk.CTkOptionMenu(
            select_frame, values=list(self.BASKET_DATA[2024].keys()),
            command=self._update, fg_color=COLORS_DARK["card_bg"], button_color=COLORS["success"]
        )
        self.family_picker.pack(side="left", padx=10)
        
        ctk.CTkLabel(select_frame, text="An:", font=FONTS["section_title"]).pack(side="left", padx=(30,10))
        
        self.year_2024_btn = ctk.CTkButton(
            select_frame, text="2024", width=80, fg_color=COLORS["success"],
            command=lambda: self._select_year(2024)
        )
        self.year_2024_btn.pack(side="left", padx=5)
        
        self.year_2025_btn = ctk.CTkButton(
            select_frame, text="2025", width=80, fg_color=COLORS_DARK["card_bg"],
            command=lambda: self._select_year(2025)
        )
        self.year_2025_btn.pack(side="left", padx=5)
        
        # Rezultat principal
        self.total_stat = CTkStatBox(self, "Total Lunar", "2,847 lei", "💰", COLORS["success"])
        self.total_stat.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.euro_stat = CTkStatBox(self, "Echivalent EUR", "€ 572", "💶", COLORS["accent"])
        self.euro_stat.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        self.desc_label = ctk.CTkLabel(self, text="", font=FONTS["caption"], text_color=COLORS_DARK["text_secondary"])
        self.desc_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Tabel comparativ
        table_card = CTkCard(self)
        table_card.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(table_card, text="📊 Comparație Tipuri Gospodării", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.comparison_table = DataTable(table_card, columns=["Tip", "RON/lună", "EUR/lună", "RON/an"], height=180)
        self.comparison_table.pack(padx=20, pady=(0,20), fill="x")
        
        # Comparație cu salariul mediu
        salary_card = CTkCard(self)
        salary_card.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(salary_card, text="💼 Comparație cu Salariul Mediu Net", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.salary_info = ctk.CTkLabel(
            salary_card, text="", font=FONTS["body"], wraplength=600, justify="left"
        )
        self.salary_info.pack(padx=20, pady=(0,20), anchor="w")
        
        # Sursă
        ctk.CTkLabel(self, text="Sursă: INS, calcule proprii cu ajustare inflație", 
                     font=FONTS["caption"], text_color=COLORS_DARK["text_secondary"]
        ).grid(row=7, column=0, columnspan=2, pady=10)
        
        self._update(self.family_picker.get())
        self._update_table()
    
    def _select_year(self, year):
        self.selected_year = year
        self.year_2024_btn.configure(fg_color=COLORS["success"] if year == 2024 else COLORS_DARK["card_bg"])
        self.year_2025_btn.configure(fg_color=COLORS["success"] if year == 2025 else COLORS_DARK["card_bg"])
        self._update(self.family_picker.get())
        self._update_table()
    
    def _update(self, family_type):
        data = self.BASKET_DATA[self.selected_year]
        ron, desc = data.get(family_type, (2847, ""))
        eur = int(ron / self.EUR_RATE)
        
        self.total_stat.set_value(f"{ron:,} lei".replace(",", " "))
        self.euro_stat.set_value(f"€ {eur:,}".replace(",", " "))
        self.desc_label.configure(text=desc)
        
        # Salariu mediu 2024: ~4500 lei net
        avg_salary = 4500 if self.selected_year == 2024 else 4900
        deficit = ron - avg_salary
        
        if deficit > 0:
            self.salary_info.configure(
                text=f"Salariu mediu net: {avg_salary:,} lei\n"
                     f"Deficit lunar: {deficit:,} lei (necesar venit suplimentar sau economii)".replace(",", " "),
                text_color=COLORS["danger"]
            )
        else:
            self.salary_info.configure(
                text=f"Salariu mediu net: {avg_salary:,} lei\n"
                     f"Diferență pozitivă: {-deficit:,} lei (posibil pentru economii)".replace(",", " "),
                text_color=COLORS["success"]
            )
    
    def _update_table(self):
        self.comparison_table.clear()
        data = self.BASKET_DATA[self.selected_year]
        
        for family, (ron, _) in data.items():
            eur = int(ron / self.EUR_RATE)
            annual = ron * 12
            self.comparison_table.add_row(
                [family, f"{ron:,}".replace(",", " "), f"€{eur}", f"{annual:,}".replace(",", " ")],
                [COLORS_DARK["text_primary"], COLORS["success"], COLORS["accent"], COLORS_DARK["text_secondary"]]
            )


# ═══════════════════════════════════════════════════════════════
# 🔥 FIRE VIEW - Simulator Pensie
# ═══════════════════════════════════════════════════════════════

class FireView(ctk.CTkScrollableFrame):
    """Simulator FIRE / Pensie complet"""
    
    def __init__(self, parent, back_command: Callable, currency_var):
        super().__init__(parent, fg_color=COLORS["fire_bg"])
        self.back_command = back_command
        self.currency_var = currency_var
        self.columnconfigure(0, weight=1)
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="🔥 Simulator FIRE / Pensie", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Explicație FIRE
        explain = CTkCard(self, fg_color=COLORS["fire_card"])
        explain.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(explain, text="Ce este FIRE?", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        explanation = """FIRE = Financial Independence, Retire Early (Independență Financiară, Pensionare Timpurie)

Regula 4% (Trinity Study, 1998):
Poți retrage 4% din portofoliu în primul an, apoi ajustezi cu inflația, 
fără a epuiza capitalul în 30 de ani (95% rată de succes istoric).

Formula FIRE: Portofoliu necesar = Cheltuieli anuale × 25

Exemple:
• Cheltuieli 2,000€/lună = 24,000€/an → Necesar: 600,000€
• Cheltuieli 3,000€/lună = 36,000€/an → Necesar: 900,000€"""
        
        ctk.CTkLabel(explain, text=explanation, font=FONTS["body"], 
                     text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left"
        ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Inputs
        inputs_card = CTkCard(self, fg_color=COLORS["fire_card"])
        inputs_card.grid(row=2, column=0, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(inputs_card, text="⚙️ Parametri Simulare", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.portfolio = CTkInputGroup(inputs_card, "Portofoliu Total", "500000", "500000")
        self.portfolio.pack(padx=20, pady=5, fill="x")
        
        self.monthly_withdrawal = CTkInputGroup(inputs_card, "Retragere Lunară Dorită", "2000", "2000")
        self.monthly_withdrawal.pack(padx=20, pady=5, fill="x")
        
        self.fire_return = CTkSliderWithLabel(
            inputs_card, label="Randament Așteptat (%)", from_=0, to=12,
            initial_value=7, suffix="%", decimals=1, progress_color=COLORS["warning"]
        )
        self.fire_return.pack(padx=20, pady=5, fill="x")
        
        self.fire_inflation = CTkSliderWithLabel(
            inputs_card, label="Inflație (%)", from_=0, to=10,
            initial_value=3, suffix="%", decimals=1, progress_color=COLORS["danger"]
        )
        self.fire_inflation.pack(padx=20, pady=5, fill="x")
        
        sim_btn = create_styled_button(inputs_card, "⚡ Simulează Pensionare", "warning", command=self._simulate)
        sim_btn.pack(padx=20, pady=20, fill="x")
        
        # Rezultate
        results_frame = ctk.CTkFrame(self, fg_color="transparent")
        results_frame.grid(row=3, column=0, sticky="ew", pady=10)
        results_frame.columnconfigure((0,1), weight=1)
        
        self.years_stat = CTkStatBox(results_frame, "Ani Sustenabili", "30+ ani", "📅", COLORS["success"])
        self.years_stat.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.rate_stat = CTkStatBox(results_frame, "Rată Retragere", "4.0%", "📊", COLORS["accent"])
        self.rate_stat.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.annual_stat = CTkStatBox(results_frame, "Retragere Anuală", "€ 24,000", "💰", COLORS["warning"])
        self.annual_stat.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.needed_stat = CTkStatBox(results_frame, "Portofoliu Necesar", "€ 600,000", "🎯", COLORS["purple"])
        self.needed_stat.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Status
        self.status_card = CTkCard(self, fg_color=COLORS["fire_card"])
        self.status_card.grid(row=4, column=0, sticky="ew", pady=10, padx=10)
        
        self.status_label = ctk.CTkLabel(self.status_card, text="", font=FONTS["subheader"], wraplength=600)
        self.status_label.pack(padx=20, pady=20)
        
        # Evoluție anuală
        yearly_card = CTkCard(self, fg_color=COLORS["fire_card"])
        yearly_card.grid(row=5, column=0, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(yearly_card, text="📈 Evoluție Portofoliu la Pensie", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.yearly_table = DataTable(yearly_card, columns=["An", "Sold Inițial", "Retragere", "Sold Final"], height=250)
        self.yearly_table.pack(padx=20, pady=(0,20), fill="x")
    
    def _simulate(self):
        portfolio = self.portfolio.get_float()
        monthly = self.monthly_withdrawal.get_float()
        annual_withdrawal = monthly * 12
        rate = self.fire_return.get() / 100
        inflation = self.fire_inflation.get() / 100
        currency = self.currency_var.get()
        
        withdrawal_rate = (annual_withdrawal / portfolio) * 100
        needed_portfolio = annual_withdrawal * 25
        
        self.rate_stat.set_value(f"{withdrawal_rate:.1f}%")
        self.annual_stat.set_value(format_currency(annual_withdrawal, currency))
        self.needed_stat.set_value(format_currency(needed_portfolio, currency))
        
        # Simulare
        balance = portfolio
        years = 0
        self.yearly_table.clear()
        
        current_withdrawal = annual_withdrawal
        
        while balance > 0 and years < 50:
            years += 1
            start_balance = balance
            balance = balance * (1 + rate) - current_withdrawal
            current_withdrawal *= (1 + inflation)
            
            if years <= 30:
                color = COLORS["success"] if balance > 0 else COLORS["danger"]
                self.yearly_table.add_row(
                    [str(years), format_currency(start_balance, currency), 
                     format_currency(current_withdrawal / (1 + inflation), currency),
                     format_currency(max(0, balance), currency)],
                    [COLORS_DARK["text_primary"], COLORS["accent"], COLORS["warning"], color]
                )
            
            if balance <= 0:
                break
        
        if years >= 30:
            self.years_stat.set_value("30+ ani ✓")
            self.years_stat.set_accent(COLORS["success"])
            self.status_label.configure(
                text="✅ FELICITĂRI! Portofoliul tău este sustenabil pentru 30+ ani de pensionare!",
                text_color=COLORS["success"]
            )
        else:
            self.years_stat.set_value(f"~{years} ani")
            self.years_stat.set_accent(COLORS["danger"])
            self.status_label.configure(
                text=f"⚠️ ATENȚIE! Portofoliul se epuizează în ~{years} ani. Redu retragerea sau mărește capitalul.",
                text_color=COLORS["danger"]
            )
