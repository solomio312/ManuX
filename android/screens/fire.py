"""
ManuX Wealth OS - FIRE Screen
Financial Independence, Retire Early simulator
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivy.metrics import dp


class FireScreen(MDScreen):
    """FIRE - Financial Independence, Retire Early"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="🔥 Simulator FIRE", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Explanation
        explain_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(180))
        explain_card.md_bg_color = (0.47, 0.21, 0.06, 1)
        explain_card.add_widget(MDLabel(
            text="FIRE = Financial Independence, Retire Early\n\n"
                 "Regula 4% (Trinity Study):\n"
                 "Poți retrage 4% din portofoliu anual fără a epuiza capitalul în 30 ani.\n\n"
                 "Formula: Portofoliu necesar = Cheltuieli anuale × 25",
            font_style="Body", role="medium"
        ))
        main_layout.add_widget(explain_card)
        
        # Inputs
        input_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(200))
        input_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        self.portfolio_input = MDTextField(mode="outlined", hint_text="Portofoliu Total (€)", text="500000")
        self.withdrawal_input = MDTextField(mode="outlined", hint_text="Retragere Lunară (€)", text="2000")
        self.return_input = MDTextField(mode="outlined", hint_text="Randament (%)", text="7")
        self.inflation_input = MDTextField(mode="outlined", hint_text="Inflație (%)", text="3")
        
        for inp in [self.portfolio_input, self.withdrawal_input, self.return_input, self.inflation_input]:
            input_layout.add_widget(inp)
        
        input_card.add_widget(input_layout)
        main_layout.add_widget(input_card)
        
        # Simulate button
        sim_btn = MDButton(
            MDButtonText(text="⚡ Simulează Pensionare"),
            style="filled",
            on_release=lambda x: self._simulate()
        )
        main_layout.add_widget(sim_btn)
        
        # Results
        results_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), spacing=dp(8))
        
        self.years_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.5)
        years_layout = MDBoxLayout(orientation='vertical')
        years_layout.add_widget(MDLabel(text="📅 Ani Sustenabili", halign="center", font_style="Body", role="small"))
        self.years_label = MDLabel(text="30+ ani", font_style="Headline", role="small", halign="center", 
                                    theme_text_color="Custom", text_color=(0.06, 0.73, 0.51, 1))
        years_layout.add_widget(self.years_label)
        self.years_card.add_widget(years_layout)
        
        self.rate_card = MDCard(style="elevated", padding=dp(12), radius=dp(12), size_hint_x=0.5)
        rate_layout = MDBoxLayout(orientation='vertical')
        rate_layout.add_widget(MDLabel(text="📊 Rată Retragere", halign="center", font_style="Body", role="small"))
        self.rate_label = MDLabel(text="4.0%", font_style="Headline", role="small", halign="center",
                                   theme_text_color="Custom", text_color=(0.23, 0.51, 0.96, 1))
        rate_layout.add_widget(self.rate_label)
        self.rate_card.add_widget(rate_layout)
        
        results_box.add_widget(self.years_card)
        results_box.add_widget(self.rate_card)
        main_layout.add_widget(results_box)
        
        # Status
        self.status_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(60))
        self.status_label = MDLabel(text="Completează datele și apasă Simulează", halign="center")
        self.status_card.add_widget(self.status_label)
        main_layout.add_widget(self.status_card)
        
        # Yearly evolution
        yearly_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(250))
        yearly_layout = MDBoxLayout(orientation='vertical')
        yearly_layout.add_widget(MDLabel(text="📈 Evoluție Portofoliu", font_style="Title", role="medium", size_hint_y=None, height=dp(40)))
        
        yearly_scroll = MDScrollView()
        self.yearly_list = MDList()
        yearly_scroll.add_widget(self.yearly_list)
        yearly_layout.add_widget(yearly_scroll)
        
        yearly_card.add_widget(yearly_layout)
        main_layout.add_widget(yearly_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _simulate(self):
        try:
            portfolio = float(self.portfolio_input.text or 500000)
            monthly = float(self.withdrawal_input.text or 2000)
            annual = monthly * 12
            rate = float(self.return_input.text or 7) / 100
            inflation = float(self.inflation_input.text or 3) / 100
            
            withdrawal_rate = (annual / portfolio) * 100
            self.rate_label.text = f"{withdrawal_rate:.1f}%"
            
            balance = portfolio
            years = 0
            current_withdrawal = annual
            
            self.yearly_list.clear_widgets()
            
            while balance > 0 and years < 50:
                years += 1
                balance = balance * (1 + rate) - current_withdrawal
                current_withdrawal *= (1 + inflation)
                
                if years <= 30:
                    item = MDListItem(
                        MDListItemHeadlineText(text=f"An {years}"),
                        MDListItemSupportingText(text=f"Sold: € {max(0, balance):,.0f}")
                    )
                    self.yearly_list.add_widget(item)
                
                if balance <= 0:
                    break
            
            if years >= 30:
                self.years_label.text = "30+ ani ✓"
                self.years_label.text_color = (0.06, 0.73, 0.51, 1)
                self.status_label.text = "✅ Portofoliul este sustenabil pentru 30+ ani!"
                self.status_card.md_bg_color = (0.02, 0.31, 0.23, 1)
            else:
                self.years_label.text = f"~{years} ani"
                self.years_label.text_color = (0.94, 0.27, 0.27, 1)
                self.status_label.text = f"⚠️ Portofoliul se epuizează în ~{years} ani"
                self.status_card.md_bg_color = (0.50, 0.12, 0.12, 1)
                
        except Exception as e:
            print(f"Error: {e}")
