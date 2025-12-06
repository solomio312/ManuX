"""
ManuX Wealth OS - Real Estate Screen
Real estate ROI calculator
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp


class RealEstateScreen(MDScreen):
    """Real estate investment calculator"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="🏠 Calculator Imobiliar", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Property inputs
        prop_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(200))
        prop_card.add_widget(MDLabel(text="🏢 Proprietate", font_style="Title", role="medium", size_hint_y=None, height=dp(30)))
        prop_layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
        
        self.price_input = MDTextField(mode="outlined", hint_text="Preț Proprietate (€)", text="100000")
        self.down_input = MDTextField(mode="outlined", hint_text="Avans (%)", text="20")
        self.rate_input = MDTextField(mode="outlined", hint_text="Dobândă Credit (%)", text="6")
        
        for inp in [self.price_input, self.down_input, self.rate_input]:
            prop_layout.add_widget(inp)
        prop_card.add_widget(prop_layout)
        main_layout.add_widget(prop_card)
        
        # Income inputs
        income_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(150))
        income_card.add_widget(MDLabel(text="💰 Venituri", font_style="Title", role="medium", size_hint_y=None, height=dp(30)))
        income_layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
        
        self.rent_input = MDTextField(mode="outlined", hint_text="Chirie Lunară (€)", text="500")
        self.vacancy_input = MDTextField(mode="outlined", hint_text="Vacanță (%)", text="5")
        
        for inp in [self.rent_input, self.vacancy_input]:
            income_layout.add_widget(inp)
        income_card.add_widget(income_layout)
        main_layout.add_widget(income_card)
        
        # Calculate
        calc_btn = MDButton(MDButtonText(text="🏠 Calculează ROI"), style="filled", on_release=lambda x: self._calculate())
        main_layout.add_widget(calc_btn)
        
        # Results
        results_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(90), spacing=dp(8))
        
        self.roi_gross_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.33)
        self.roi_gross_card.md_bg_color = (0.23, 0.51, 0.96, 1)
        roi_gross_layout = MDBoxLayout(orientation='vertical')
        roi_gross_layout.add_widget(MDLabel(text="ROI Brut", halign="center", font_style="Body", role="small"))
        self.roi_gross_label = MDLabel(text="0%", halign="center", font_style="Title", role="medium")
        roi_gross_layout.add_widget(self.roi_gross_label)
        self.roi_gross_card.add_widget(roi_gross_layout)
        
        self.roi_net_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.33)
        self.roi_net_card.md_bg_color = (0.06, 0.73, 0.51, 1)
        roi_net_layout = MDBoxLayout(orientation='vertical')
        roi_net_layout.add_widget(MDLabel(text="ROI Net", halign="center", font_style="Body", role="small"))
        self.roi_net_label = MDLabel(text="0%", halign="center", font_style="Title", role="medium")
        roi_net_layout.add_widget(self.roi_net_label)
        self.roi_net_card.add_widget(roi_net_layout)
        
        self.coc_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.33)
        self.coc_card.md_bg_color = (0.55, 0.36, 0.96, 1)
        coc_layout = MDBoxLayout(orientation='vertical')
        coc_layout.add_widget(MDLabel(text="Cash-on-Cash", halign="center", font_style="Body", role="small"))
        self.coc_label = MDLabel(text="0%", halign="center", font_style="Title", role="medium")
        coc_layout.add_widget(self.coc_label)
        self.coc_card.add_widget(coc_layout)
        
        results_row.add_widget(self.roi_gross_card)
        results_row.add_widget(self.roi_net_card)
        results_row.add_widget(self.coc_card)
        main_layout.add_widget(results_row)
        
        # Details
        details_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(150))
        self.details_layout = MDBoxLayout(orientation='vertical', spacing=dp(4))
        self.mortgage_label = MDLabel(text="Rată Lunară: € 0", font_style="Body", role="medium")
        self.cashflow_label = MDLabel(text="Cashflow Net: € 0/lună", font_style="Body", role="medium")
        self.annual_label = MDLabel(text="Venit Anual Net: € 0", font_style="Body", role="medium")
        for lbl in [self.mortgage_label, self.cashflow_label, self.annual_label]:
            self.details_layout.add_widget(lbl)
        details_card.add_widget(self.details_layout)
        main_layout.add_widget(details_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _calculate(self):
        try:
            price = float(self.price_input.text or 100000)
            down_pct = float(self.down_input.text or 20) / 100
            mortgage_rate = float(self.rate_input.text or 6) / 100 / 12
            rent = float(self.rent_input.text or 500)
            vacancy_pct = float(self.vacancy_input.text or 5) / 100
            
            down_payment = price * down_pct
            loan = price - down_payment
            
            # Mortgage calculation
            if mortgage_rate > 0:
                n = 25 * 12
                mortgage = loan * (mortgage_rate * (1 + mortgage_rate)**n) / ((1 + mortgage_rate)**n - 1)
            else:
                mortgage = loan / 300
            
            gross_annual = rent * 12
            vacancy_loss = gross_annual * vacancy_pct
            effective = gross_annual - vacancy_loss
            
            roi_gross = (gross_annual / price) * 100
            roi_net = (effective / price) * 100
            
            net_cashflow = effective - (mortgage * 12)
            coc = (net_cashflow / down_payment) * 100 if down_payment > 0 else 0
            
            self.roi_gross_label.text = f"{roi_gross:.1f}%"
            self.roi_net_label.text = f"{roi_net:.1f}%"
            self.coc_label.text = f"{coc:.1f}%"
            
            self.mortgage_label.text = f"Rată Lunară: € {mortgage:,.0f}"
            self.cashflow_label.text = f"Cashflow Net: € {net_cashflow/12:,.0f}/lună"
            self.annual_label.text = f"Venit Anual Net: € {net_cashflow:,.0f}"
            
        except Exception as e:
            print(f"Error: {e}")
