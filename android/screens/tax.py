"""
ManuX Wealth OS - Tax Screen
Tax calculator for Romania, Canada, USA
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivy.metrics import dp


class TaxScreen(MDScreen):
    """Tax calculator for multiple countries"""
    
    TAX_INFO = {
        "România": {
            "color": (0.50, 0.12, 0.12, 1),
            "info": "• Impozit câștig capital: 10%\n• Impozit dividende: 8%\n• CASS: 10% dacă > 6 salarii minime"
        },
        "Canada": {
            "color": (0.50, 0.12, 0.12, 1),
            "info": "• Capital gains: 50% inclusion\n• Dividende: credit ~15-25%\n• TFSA/RRSP: conturi avantajoase"
        },
        "SUA": {
            "color": (0.50, 0.12, 0.12, 1),
            "info": "• Short-term (<1an): 10-37%\n• Long-term (>1an): 0-20%\n• NIIT: +3.8% peste $200k"
        }
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_country = "România"
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="💸 Calculator Taxe", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Country selector
        country_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(8))
        self.country_buttons = {}
        for country in ["România", "Canada", "SUA"]:
            btn = MDButton(
                MDButtonText(text=country),
                style="filled" if country == self.selected_country else "outlined",
                size_hint_x=0.33,
                on_release=lambda x, c=country: self._select_country(c)
            )
            self.country_buttons[country] = btn
            country_box.add_widget(btn)
        main_layout.add_widget(country_box)
        
        # Info card
        self.info_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(120))
        self.info_card.md_bg_color = (0.50, 0.12, 0.12, 1)
        self.info_label = MDLabel(text=self.TAX_INFO["România"]["info"], font_style="Body", role="medium")
        self.info_card.add_widget(self.info_label)
        main_layout.add_widget(self.info_card)
        
        # Inputs
        input_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(140))
        input_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        self.profit_input = MDTextField(mode="outlined", hint_text="Câștig Capital", text="50000")
        self.dividends_input = MDTextField(mode="outlined", hint_text="Dividende", text="5000")
        
        input_layout.add_widget(self.profit_input)
        input_layout.add_widget(self.dividends_input)
        input_card.add_widget(input_layout)
        main_layout.add_widget(input_card)
        
        # Calculate
        calc_btn = MDButton(MDButtonText(text="💸 Calculează Taxe"), style="filled", on_release=lambda x: self._calculate())
        main_layout.add_widget(calc_btn)
        
        # Results
        results_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(90), spacing=dp(8))
        
        self.cap_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.5)
        self.cap_card.md_bg_color = (0.94, 0.27, 0.27, 1)
        cap_layout = MDBoxLayout(orientation='vertical')
        cap_layout.add_widget(MDLabel(text="Taxă Capital", halign="center", font_style="Body", role="small"))
        self.cap_label = MDLabel(text="€ 0", halign="center", font_style="Title", role="medium")
        cap_layout.add_widget(self.cap_label)
        self.cap_card.add_widget(cap_layout)
        
        self.div_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.5)
        self.div_card.md_bg_color = (0.96, 0.62, 0.04, 1)
        div_layout = MDBoxLayout(orientation='vertical')
        div_layout.add_widget(MDLabel(text="Taxă Dividende", halign="center", font_style="Body", role="small"))
        self.div_label = MDLabel(text="€ 0", halign="center", font_style="Title", role="medium")
        div_layout.add_widget(self.div_label)
        self.div_card.add_widget(div_layout)
        
        results_row.add_widget(self.cap_card)
        results_row.add_widget(self.div_card)
        main_layout.add_widget(results_row)
        
        # Total
        total_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(80))
        total_card.md_bg_color = (0.94, 0.27, 0.27, 1)
        total_layout = MDBoxLayout(orientation='vertical')
        total_layout.add_widget(MDLabel(text="💸 TOTAL TAXE", halign="center", font_style="Title", role="medium"))
        self.total_label = MDLabel(text="€ 0", halign="center", font_style="Headline", role="small")
        total_layout.add_widget(self.total_label)
        total_card.add_widget(total_layout)
        main_layout.add_widget(total_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _select_country(self, country):
        self.selected_country = country
        for c, btn in self.country_buttons.items():
            btn.style = "filled" if c == country else "outlined"
        self.info_label.text = self.TAX_INFO[country]["info"]
    
    def _calculate(self):
        try:
            profit = float(self.profit_input.text or 0)
            dividends = float(self.dividends_input.text or 0)
            
            if self.selected_country == "România":
                tax_cap = profit * 0.10
                tax_div = dividends * 0.08
                currency = "lei"
            elif self.selected_country == "Canada":
                tax_cap = profit * 0.50 * 0.30
                tax_div = dividends * 0.25
                currency = "CAD"
            else:  # USA
                tax_cap = profit * 0.15
                tax_div = dividends * 0.15
                currency = "USD"
            
            total = tax_cap + tax_div
            
            self.cap_label.text = f"{tax_cap:,.0f} {currency}"
            self.div_label.text = f"{tax_div:,.0f} {currency}"
            self.total_label.text = f"{total:,.0f} {currency}"
            
        except Exception as e:
            print(f"Error: {e}")
