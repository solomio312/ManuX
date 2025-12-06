"""
ManuX Wealth OS - Module Views Part 2 (Real Estate, Rebalance, Tax, Guide)
"""

import customtkinter as ctk
from typing import Callable

from theme_styles import COLORS, COLORS_DARK, FONTS, format_currency, format_percentage, create_styled_button
from widgets import CTkCard, CTkStatBox, CTkSliderWithLabel, CTkInputGroup, DataTable


# ═══════════════════════════════════════════════════════════════
# 🏠 REAL ESTATE VIEW - Calculator Imobiliar
# ═══════════════════════════════════════════════════════════════

class RealEstateView(ctk.CTkScrollableFrame):
    """Calculator ROI Imobiliar complet"""
    
    def __init__(self, parent, back_command: Callable, currency_var):
        super().__init__(parent, fg_color="transparent")
        self.back_command = back_command
        self.currency_var = currency_var
        self.columnconfigure((0,1), weight=1)
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="🏠 Calculator Imobiliar", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Explicație
        explain = CTkCard(self)
        explain.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(explain, text="Analiza Investiției Imobiliare", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        explanation = """Calculatorul analizează randamentul investiției imobiliare considerând:
• ROI Brut = Chirie anuală / Preț proprietate
• ROI Net = (Chirie - Cheltuieli) / Investiție proprie (avans)
• Cash-on-Cash Return = Flux net de numerar / Capital investit"""
        
        ctk.CTkLabel(explain, text=explanation, font=FONTS["body"], 
                     text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left"
        ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Inputs - Proprietate
        prop_card = CTkCard(self)
        prop_card.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(prop_card, text="🏢 Detalii Proprietate", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        inputs_frame = ctk.CTkFrame(prop_card, fg_color="transparent")
        inputs_frame.pack(padx=20, pady=(0,20), fill="x")
        inputs_frame.columnconfigure((0,1), weight=1)
        
        self.price = CTkInputGroup(inputs_frame, "Preț Proprietate (€)", "100000", "100000")
        self.price.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.down_payment = CTkInputGroup(inputs_frame, "Avans (%)", "20", "20")
        self.down_payment.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.mortgage_rate = CTkInputGroup(inputs_frame, "Dobândă Credit (%/an)", "6", "6")
        self.mortgage_rate.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.mortgage_years = CTkInputGroup(inputs_frame, "Durată Credit (ani)", "25", "25")
        self.mortgage_years.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Inputs - Venituri & Cheltuieli
        income_card = CTkCard(self)
        income_card.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(income_card, text="💰 Venituri și Cheltuieli", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        income_frame = ctk.CTkFrame(income_card, fg_color="transparent")
        income_frame.pack(padx=20, pady=(0,20), fill="x")
        income_frame.columnconfigure((0,1), weight=1)
        
        self.rent = CTkInputGroup(income_frame, "Chirie Lunară (€)", "500", "500")
        self.rent.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.vacancy = CTkInputGroup(income_frame, "Vacanță (%/an)", "5", "5")
        self.vacancy.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.maintenance = CTkInputGroup(income_frame, "Mentenanță (%)", "10", "10")
        self.maintenance.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.property_tax = CTkInputGroup(income_frame, "Taxe Proprietate (€/an)", "500", "500")
        self.property_tax.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.insurance = CTkInputGroup(income_frame, "Asigurare (€/an)", "300", "300")
        self.insurance.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        self.appreciation = CTkInputGroup(income_frame, "Apreciere Anuală (%)", "3", "3")
        self.appreciation.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        calc_btn = create_styled_button(self, "🏠 Calculează ROI Complet", "cyan", command=self._calculate)
        calc_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Rezultate
        results_frame = ctk.CTkFrame(self, fg_color="transparent")
        results_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        results_frame.columnconfigure((0,1,2), weight=1)
        
        self.roi_gross = CTkStatBox(results_frame, "ROI Brut", "0%", "📊", COLORS["accent"])
        self.roi_gross.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.roi_net = CTkStatBox(results_frame, "ROI Net", "0%", "📈", COLORS["success"])
        self.roi_net.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.cash_on_cash = CTkStatBox(results_frame, "Cash-on-Cash", "0%", "💰", COLORS["purple"])
        self.cash_on_cash.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        self.mortgage_monthly = CTkStatBox(results_frame, "Rată Lunară", "€ 0", "🏦", COLORS["warning"])
        self.mortgage_monthly.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.net_income = CTkStatBox(results_frame, "Venit Net Lunar", "€ 0", "💵", COLORS["success"])
        self.net_income.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.annual_cashflow = CTkStatBox(results_frame, "Cashflow Anual", "€ 0", "📅", COLORS["cyan"])
        self.annual_cashflow.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        # Detalii
        details_card = CTkCard(self)
        details_card.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        
        ctk.CTkLabel(details_card, text="📋 Breakdown Anual", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.details_table = DataTable(details_card, 
            columns=["Categorie", "Lunar", "Anual"], height=200
        )
        self.details_table.pack(padx=20, pady=(0,20), fill="x")
    
    def _calculate(self):
        currency = self.currency_var.get()
        
        price = self.price.get_float()
        down_pct = self.down_payment.get_float() / 100
        mortgage_rate = self.mortgage_rate.get_float() / 100 / 12
        mortgage_years = int(self.mortgage_years.get_float())
        
        rent = self.rent.get_float()
        vacancy_pct = self.vacancy.get_float() / 100
        maintenance_pct = self.maintenance.get_float() / 100
        prop_tax = self.property_tax.get_float()
        insurance = self.insurance.get_float()
        
        # Calcule
        down_payment = price * down_pct
        loan_amount = price - down_payment
        
        # Rată ipotecară (formula PMT)
        if mortgage_rate > 0:
            n_payments = mortgage_years * 12
            mortgage_payment = loan_amount * (mortgage_rate * (1 + mortgage_rate)**n_payments) / ((1 + mortgage_rate)**n_payments - 1)
        else:
            mortgage_payment = loan_amount / (mortgage_years * 12)
        
        # Venituri și cheltuieli
        gross_rent_annual = rent * 12
        vacancy_loss = gross_rent_annual * vacancy_pct
        effective_rent = gross_rent_annual - vacancy_loss
        
        maintenance_cost = effective_rent * maintenance_pct
        total_expenses = maintenance_cost + prop_tax + insurance + (mortgage_payment * 12)
        
        net_operating_income = effective_rent - maintenance_cost - prop_tax - insurance
        net_cashflow = net_operating_income - (mortgage_payment * 12)
        
        # ROI
        roi_gross = (gross_rent_annual / price) * 100
        roi_net = (net_operating_income / price) * 100
        cash_on_cash = (net_cashflow / down_payment) * 100 if down_payment > 0 else 0
        
        # Update UI
        self.roi_gross.set_value(f"{roi_gross:.1f}%")
        self.roi_net.set_value(f"{roi_net:.1f}%")
        self.cash_on_cash.set_value(f"{cash_on_cash:.1f}%")
        self.mortgage_monthly.set_value(format_currency(mortgage_payment, currency))
        self.net_income.set_value(format_currency(net_cashflow / 12, currency))
        self.annual_cashflow.set_value(format_currency(net_cashflow, currency))
        
        # Table
        self.details_table.clear()
        rows = [
            ("Chirie Brută", rent, gross_rent_annual, COLORS["success"]),
            ("(-) Vacanță", vacancy_loss/12, vacancy_loss, COLORS["warning"]),
            ("(-) Mentenanță", maintenance_cost/12, maintenance_cost, COLORS["warning"]),
            ("(-) Taxe", prop_tax/12, prop_tax, COLORS["danger"]),
            ("(-) Asigurare", insurance/12, insurance, COLORS["danger"]),
            ("(-) Rată Credit", mortgage_payment, mortgage_payment*12, COLORS["danger"]),
            ("= Cashflow Net", net_cashflow/12, net_cashflow, COLORS["success"] if net_cashflow > 0 else COLORS["danger"]),
        ]
        
        for cat, monthly, annual, color in rows:
            self.details_table.add_row(
                [cat, format_currency(monthly, currency), format_currency(annual, currency)],
                [COLORS_DARK["text_primary"], color, color]
            )


# ═══════════════════════════════════════════════════════════════
# ⚖️ REBALANCE VIEW - Rebalansare Portofoliu
# ═══════════════════════════════════════════════════════════════

class RebalanceView(ctk.CTkScrollableFrame):
    """Calculator rebalansare portofoliu"""
    
    def __init__(self, parent, back_command: Callable, currency_var):
        super().__init__(parent, fg_color="transparent")
        self.back_command = back_command
        self.currency_var = currency_var
        self.columnconfigure(0, weight=1)
        self.assets = []
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="⚖️ Rebalansare Portofoliu", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Explicație
        explain = CTkCard(self)
        explain.grid(row=1, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(explain, text="Ce este Rebalansarea?", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        explanation = """Rebalansarea înseamnă ajustarea portofoliului pentru a reveni la alocarea țintă.
        
Exemplu: Dacă ținta ta e 80% Acțiuni / 20% Obligațiuni, dar acțiunile au crescut 
și acum ai 90% Acțiuni / 10% Obligațiuni, vinzi acțiuni și cumperi obligațiuni.

Rebalansarea:
• Reduce riscul prin menținerea diversificării
• Forțează "cumpără jos, vinde sus"
• Recomandată anual sau când deviația e > 5%"""
        
        ctk.CTkLabel(explain, text=explanation, font=FONTS["body"], 
                     text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left"
        ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Input total portofoliu
        total_card = CTkCard(self)
        total_card.grid(row=2, column=0, sticky="ew", pady=10)
        
        self.total_portfolio = CTkInputGroup(total_card, "Valoare Totală Portofoliu", "100000", "100000")
        self.total_portfolio.pack(padx=20, pady=20, fill="x")
        
        # Add asset form
        add_card = CTkCard(self)
        add_card.grid(row=3, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(add_card, text="➕ Adaugă Asset", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        form_frame = ctk.CTkFrame(add_card, fg_color="transparent")
        form_frame.pack(padx=20, pady=(0,20), fill="x")
        form_frame.columnconfigure((0,1,2), weight=1)
        
        self.asset_name = CTkInputGroup(form_frame, "Nume Asset", "VWCE")
        self.asset_name.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.asset_current = CTkInputGroup(form_frame, "Valoare Actuală", "50000")
        self.asset_current.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.asset_target = CTkInputGroup(form_frame, "Țintă (%)", "60")
        self.asset_target.grid(row=0, column=2, padx=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(add_card, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(0,20), fill="x")
        
        create_styled_button(btn_frame, "➕ Adaugă", "success", width=120, command=self._add_asset).pack(side="left", padx=5)
        create_styled_button(btn_frame, "🗑️ Șterge Tot", "danger", width=120, command=self._clear_assets).pack(side="left", padx=5)
        create_styled_button(btn_frame, "⚖️ Calculează", "primary", width=120, command=self._calculate).pack(side="right", padx=5)
        
        # Assets table
        table_card = CTkCard(self)
        table_card.grid(row=4, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(table_card, text="📊 Portofoliu Curent", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.assets_table = DataTable(table_card, 
            columns=["Asset", "Actual", "% Actual", "Țintă", "% Țintă", "Acțiune"], height=200
        )
        self.assets_table.pack(padx=20, pady=(0,20), fill="x")
        
        # Sumar
        self.summary_label = ctk.CTkLabel(self, text="", font=FONTS["body"], wraplength=600)
        self.summary_label.grid(row=5, column=0, pady=20)
        
        # Presetting default assets
        self._preset_assets()
    
    def _preset_assets(self):
        defaults = [
            ("VWCE (Acțiuni)", 60000, 60),
            ("AGGH (Obligațiuni)", 25000, 30),
            ("Cash", 15000, 10),
        ]
        for name, current, target in defaults:
            self.assets.append({"name": name, "current": current, "target": target})
        self._update_table()
    
    def _add_asset(self):
        name = self.asset_name.get()
        current = self.asset_current.get_float()
        target = self.asset_target.get_float()
        
        if name and current >= 0 and target >= 0:
            self.assets.append({"name": name, "current": current, "target": target})
            self._update_table()
    
    def _clear_assets(self):
        self.assets = []
        self._update_table()
    
    def _update_table(self):
        self.assets_table.clear()
        total = sum(a["current"] for a in self.assets)
        currency = self.currency_var.get()
        
        for asset in self.assets:
            current_pct = (asset["current"] / total * 100) if total > 0 else 0
            target_pct = asset["target"]
            diff = current_pct - target_pct
            
            if diff > 1:
                action = f"Vinde {diff:.1f}%"
                color = COLORS["danger"]
            elif diff < -1:
                action = f"Cumpără {-diff:.1f}%"
                color = COLORS["success"]
            else:
                action = "OK ✓"
                color = COLORS["success"]
            
            self.assets_table.add_row(
                [asset["name"], format_currency(asset["current"], currency), 
                 f"{current_pct:.1f}%", format_currency(total * target_pct / 100, currency),
                 f"{target_pct:.0f}%", action],
                [COLORS_DARK["text_primary"], COLORS["accent"], COLORS["purple"], 
                 COLORS["warning"], COLORS["warning"], color]
            )
    
    def _calculate(self):
        total = self.total_portfolio.get_float()
        currency = self.currency_var.get()
        
        # Update actual values based on total
        actual_total = sum(a["current"] for a in self.assets)
        if actual_total != total and actual_total > 0:
            ratio = total / actual_total
            for asset in self.assets:
                asset["current"] *= ratio
        
        self._update_table()
        
        total_target = sum(a["target"] for a in self.assets)
        if abs(total_target - 100) > 0.1:
            self.summary_label.configure(
                text=f"⚠️ Atenție: Totalul țintelor este {total_target:.1f}% (ar trebui să fie 100%)",
                text_color=COLORS["warning"]
            )
        else:
            self.summary_label.configure(
                text=f"✅ Portofoliu total: {format_currency(total, currency)} | Ținte valide (100%)",
                text_color=COLORS["success"]
            )


# ═══════════════════════════════════════════════════════════════
# 💸 TAX VIEW - Calculator Taxe (RO, CA, US)
# ═══════════════════════════════════════════════════════════════

class TaxView(ctk.CTkScrollableFrame):
    """Calculator taxe pentru România, Canada și SUA"""
    
    def __init__(self, parent, back_command: Callable):
        super().__init__(parent, fg_color=COLORS["tax_danger_bg"])
        self.back_command = back_command
        self.columnconfigure(0, weight=1)
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="💸 Calculator Taxe Investiții", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Selector țară
        country_frame = ctk.CTkFrame(self, fg_color="transparent")
        country_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(country_frame, text="Selectează Țara:", font=FONTS["section_title"]).pack(side="left", padx=10)
        
        self.country_var = ctk.StringVar(value="România")
        
        for country in ["România", "Canada", "SUA"]:
            ctk.CTkRadioButton(
                country_frame, text=country, variable=self.country_var, value=country,
                command=self._update_info
            ).pack(side="left", padx=10)
        
        # Info card
        self.info_card = CTkCard(self, fg_color=COLORS["tax_danger_card"])
        self.info_card.grid(row=2, column=0, sticky="ew", pady=10, padx=10)
        
        self.info_title = ctk.CTkLabel(self.info_card, text="", font=FONTS["subheader"])
        self.info_title.pack(padx=20, pady=(20,10), anchor="w")
        
        self.info_text = ctk.CTkLabel(self.info_card, text="", font=FONTS["body"], 
                                       text_color=COLORS_DARK["text_secondary"], wraplength=600, justify="left")
        self.info_text.pack(padx=20, pady=(0,20), anchor="w")
        
        # Inputs
        inputs_card = CTkCard(self, fg_color=COLORS["tax_danger_card"])
        inputs_card.grid(row=3, column=0, sticky="ew", pady=10, padx=10)
        
        ctk.CTkLabel(inputs_card, text="📝 Date Financiare", font=FONTS["subheader"]).pack(padx=20, pady=(20,10), anchor="w")
        
        self.profit = CTkInputGroup(inputs_card, "Câștig de Capital (profit realizat)", "50000", "50000")
        self.profit.pack(padx=20, pady=5, fill="x")
        
        self.dividends = CTkInputGroup(inputs_card, "Dividende Primite", "5000", "5000")
        self.dividends.pack(padx=20, pady=5, fill="x")
        
        self.holding_period = ctk.CTkOptionMenu(
            inputs_card, values=["< 1 an (short-term)", "> 1 an (long-term)"],
            fg_color=COLORS_DARK["card_bg"], button_color=COLORS["danger"]
        )
        self.holding_period.pack(padx=20, pady=10)
        
        calc_btn = create_styled_button(inputs_card, "💸 Calculează Taxe", "danger", command=self._calculate)
        calc_btn.pack(padx=20, pady=20, fill="x")
        
        # Rezultate
        results_frame = ctk.CTkFrame(self, fg_color="transparent")
        results_frame.grid(row=4, column=0, sticky="ew", pady=10)
        results_frame.columnconfigure((0,1), weight=1)
        
        self.tax_capital = CTkStatBox(results_frame, "Taxă Câștig Capital", "0", "📊", COLORS["danger"])
        self.tax_capital.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tax_dividends = CTkStatBox(results_frame, "Taxă Dividende", "0", "💰", COLORS["warning"])
        self.tax_dividends.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        self.tax_other = CTkStatBox(results_frame, "Alte Taxe (CASS/etc)", "0", "📋", COLORS["purple"])
        self.tax_other.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tax_total = CTkStatBox(results_frame, "TOTAL TAXE", "0", "💸", COLORS["danger"])
        self.tax_total.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        
        self._update_info()
    
    def _update_info(self):
        country = self.country_var.get()
        
        info = {
            "România": (
                "🇷🇴 Taxe pe Investiții în România",
                """• Impozit pe câștig de capital: 10% (flat)
• Impozit pe dividende: 8%
• CASS (contribuție sănătate): 10% dacă câștigul > 6 salarii minime (~21,600 lei)
• Termen plată: 25 mai anul următor
• Declarație: Declarația Unică (D212)

NOTĂ: ETF-urile cu acumulare (acc) nu generează taxă pe dividende reinvestite."""
            ),
            "Canada": (
                "🇨🇦 Taxe pe Investiții în Canada",
                """• Capital gains: 50% din câștig e impozabil la rata marginală
• Dividende eligibile: Credit taxă ~15-25%
• TFSA: Cont fără taxe (limită ~$7,000/an)
• RRSP: Cont cu taxare amânată (pensie)
• Holding > 1 an: Nu există diferență în Canada

NOTĂ: Dividendele din SUA au reținere la sursă 15% (tratat fiscal)."""
            ),
            "SUA": (
                "🇺🇸 Taxe pe Investiții în SUA",
                """• Short-term capital gains (< 1 an): Rată ordinară (10-37%)
• Long-term capital gains (> 1 an): 0%, 15%, sau 20%
• Qualified dividends: Tratate ca long-term gains
• Net Investment Income Tax: +3.8% dacă venit > $200k

Rate Long-Term Capital Gains 2024:
• 0% dacă venit < $47,025
• 15% dacă venit $47,026 - $518,900
• 20% dacă venit > $518,900"""
            )
        }
        
        title, text = info.get(country, ("", ""))
        self.info_title.configure(text=title)
        self.info_text.configure(text=text)
    
    def _calculate(self):
        country = self.country_var.get()
        profit = self.profit.get_float()
        dividends = self.dividends.get_float()
        is_long = "long" in self.holding_period.get().lower()
        
        if country == "România":
            # România
            tax_cap = profit * 0.10
            tax_div = dividends * 0.08
            # CASS dacă > 6 salarii minime
            cass = profit * 0.10 if profit > 21600 else 0
            total = tax_cap + tax_div + cass
            currency = "lei"
            
            self.tax_capital.set_value(f"{tax_cap:,.0f} {currency}")
            self.tax_dividends.set_value(f"{tax_div:,.0f} {currency}")
            self.tax_other.set_value(f"{cass:,.0f} {currency} (CASS)")
            self.tax_total.set_value(f"{total:,.0f} {currency}")
            
        elif country == "Canada":
            # Canada - 50% inclusion rate
            taxable_gain = profit * 0.50
            # Assume 30% marginal rate
            tax_cap = taxable_gain * 0.30
            # Dividende cu credit
            tax_div = dividends * 0.25
            total = tax_cap + tax_div
            currency = "CAD"
            
            self.tax_capital.set_value(f"${tax_cap:,.0f} {currency}")
            self.tax_dividends.set_value(f"${tax_div:,.0f} {currency}")
            self.tax_other.set_value("$0 (N/A)")
            self.tax_total.set_value(f"${total:,.0f} {currency}")
            
        else:  # SUA
            # USA
            if is_long:
                # Long-term (assume 15% rate)
                tax_cap = profit * 0.15
            else:
                # Short-term (assume 24% marginal)
                tax_cap = profit * 0.24
            
            tax_div = dividends * 0.15  # Qualified dividends
            # NIIT dacă venit mare
            niit = (profit + dividends) * 0.038 if (profit + dividends) > 200000 else 0
            total = tax_cap + tax_div + niit
            currency = "USD"
            
            self.tax_capital.set_value(f"${tax_cap:,.0f}")
            self.tax_dividends.set_value(f"${tax_div:,.0f}")
            self.tax_other.set_value(f"${niit:,.0f} (NIIT)")
            self.tax_total.set_value(f"${total:,.0f}")
