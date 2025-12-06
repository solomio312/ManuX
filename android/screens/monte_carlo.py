"""
ManuX Wealth OS - Monte Carlo Screen
Monte Carlo simulation for investment projections
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivy.metrics import dp
from kivy.clock import Clock
import random


class MonteCarloScreen(MDScreen):
    """Monte Carlo simulation screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(12),
            adaptive_height=True
        )
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="🎲 Monte Carlo", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Explanation
        explain_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(150))
        explain_card.add_widget(MDLabel(
            text="Simularea Monte Carlo rulează mii de scenarii posibile pentru investițiile tale, "
                 "considerând volatilitatea pieței.\n\n"
                 "• P10 (Pesimist): 10% au rezultat mai rău\n"
                 "• P50 (Median): Rezultat mediu\n"
                 "• P90 (Optimist): Doar 10% au fost mai bine",
            font_style="Body",
            role="medium"
        ))
        main_layout.add_widget(explain_card)
        
        # Inputs
        input_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(280))
        input_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        self.capital_input = MDTextField(mode="outlined", hint_text="Capital Inițial", text="10000")
        self.monthly_input = MDTextField(mode="outlined", hint_text="Depozit Lunar", text="500")
        self.years_input = MDTextField(mode="outlined", hint_text="Ani", text="20")
        self.volatility_input = MDTextField(mode="outlined", hint_text="Volatilitate (%)", text="15")
        self.sims_input = MDTextField(mode="outlined", hint_text="Nr. Simulări", text="1000")
        
        for inp in [self.capital_input, self.monthly_input, self.years_input, self.volatility_input, self.sims_input]:
            input_layout.add_widget(inp)
        
        input_card.add_widget(input_layout)
        main_layout.add_widget(input_card)
        
        # Progress
        self.progress = MDLinearProgressIndicator(size_hint_y=None, height=dp(4))
        main_layout.add_widget(self.progress)
        
        # Run button
        run_btn = MDButton(
            MDButtonIcon(icon="play"),
            MDButtonText(text="Rulează Simulare"),
            style="filled",
            on_release=lambda x: self._run_simulation()
        )
        main_layout.add_widget(run_btn)
        
        # Results
        results_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(200))
        results_layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
        
        self.p10_label = MDLabel(text="P10 (Pesimist): -", theme_text_color="Custom", text_color=(0.94, 0.27, 0.27, 1))
        self.p50_label = MDLabel(text="P50 (Median): -", theme_text_color="Custom", text_color=(0.23, 0.51, 0.96, 1))
        self.p90_label = MDLabel(text="P90 (Optimist): -", theme_text_color="Custom", text_color=(0.06, 0.73, 0.51, 1))
        self.mean_label = MDLabel(text="Media: -", theme_text_color="Custom", text_color=(0.55, 0.36, 0.96, 1))
        self.success_label = MDLabel(text="Rată Succes: -", font_style="Title", role="medium")
        
        for lbl in [self.p10_label, self.p50_label, self.p90_label, self.mean_label, self.success_label]:
            results_layout.add_widget(lbl)
        
        results_card.add_widget(results_layout)
        main_layout.add_widget(results_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _run_simulation(self):
        try:
            capital = float(self.capital_input.text or 10000)
            monthly = float(self.monthly_input.text or 500)
            years = int(self.years_input.text or 20)
            volatility = float(self.volatility_input.text or 15) / 100
            n_sims = int(self.sims_input.text or 1000)
            rate = 0.07
            
            total_invested = capital + monthly * 12 * years
            results = []
            
            for i in range(n_sims):
                total = capital
                for year in range(years):
                    yearly_return = random.gauss(rate, volatility)
                    total = total * (1 + yearly_return) + monthly * 12
                results.append(total)
                
                if i % 100 == 0:
                    self.progress.value = i / n_sims
            
            self.progress.value = 1
            results.sort()
            
            p10 = results[int(n_sims * 0.1)]
            p50 = results[int(n_sims * 0.5)]
            p90 = results[int(n_sims * 0.9)]
            mean_val = sum(results) / n_sims
            success_rate = sum(1 for r in results if r > total_invested) / n_sims * 100
            
            self.p10_label.text = f"P10 (Pesimist): € {p10:,.0f}"
            self.p50_label.text = f"P50 (Median): € {p50:,.0f}"
            self.p90_label.text = f"P90 (Optimist): € {p90:,.0f}"
            self.mean_label.text = f"Media: € {mean_val:,.0f}"
            self.success_label.text = f"Rată Succes: {success_rate:.1f}%"
            
        except Exception as e:
            print(f"Error: {e}")
