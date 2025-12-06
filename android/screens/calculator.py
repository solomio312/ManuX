"""
ManuX Wealth OS - Calculator Screen
Investment projection calculator with collapsible inputs
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivy.metrics import dp


class StatCard(MDCard):
    """Card for displaying a statistic"""
    
    def __init__(self, title, value, icon, color, **kwargs):
        super().__init__(**kwargs)
        self.style = "elevated"
        self.size_hint_x = 0.48
        self.size_hint_y = None
        self.height = dp(90)
        self.padding = dp(12)
        self.radius = dp(12)
        self.md_bg_color = (0.2, 0.25, 0.33, 1)
        
        layout = MDBoxLayout(orientation='vertical', spacing=dp(4))
        
        # Header with icon
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))
        header.add_widget(MDLabel(text=icon, font_style="Title", role="medium"))
        header.add_widget(MDLabel(text=title, font_style="Body", role="small", theme_text_color="Secondary"))
        layout.add_widget(header)
        
        # Value
        self.value_label = MDLabel(
            text=value,
            font_style="Headline",
            role="small",
            theme_text_color="Custom",
            text_color=color
        )
        layout.add_widget(self.value_label)
        
        self.add_widget(layout)
    
    def set_value(self, value):
        self.value_label.text = value


class CalculatorScreen(MDScreen):
    """Investment calculator with collapsible input sections"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        # Main scroll
        scroll = MDScrollView()
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(12),
            adaptive_height=True
        )
        
        # Header with back button
        header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            spacing=dp(8)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self._go_back()
        )
        header.add_widget(back_btn)
        
        header.add_widget(MDLabel(
            text="🧮 Calculator Investiții",
            font_style="Headline",
            role="small"
        ))
        main_layout.add_widget(header)
        
        # Input Card
        input_card = MDCard(
            style="elevated",
            padding=dp(16),
            radius=dp(16),
            size_hint_y=None,
            height=dp(320)
        )
        
        input_layout = MDBoxLayout(orientation='vertical', spacing=dp(12))
        
        # Capital initial
        self.capital_input = MDTextField(
            mode="outlined",
            hint_text="Capital Inițial",
            text="10000",
            input_filter="float"
        )
        input_layout.add_widget(self.capital_input)
        
        # Depozit lunar
        self.monthly_input = MDTextField(
            mode="outlined",
            hint_text="Depozit Lunar",
            text="500",
            input_filter="float"
        )
        input_layout.add_widget(self.monthly_input)
        
        # Ani
        self.years_input = MDTextField(
            mode="outlined",
            hint_text="Durată (ani)",
            text="20",
            input_filter="int"
        )
        input_layout.add_widget(self.years_input)
        
        # Dobândă
        self.rate_input = MDTextField(
            mode="outlined",
            hint_text="Dobândă Anuală (%)",
            text="7",
            input_filter="float"
        )
        input_layout.add_widget(self.rate_input)
        
        # Inflație
        self.inflation_input = MDTextField(
            mode="outlined",
            hint_text="Inflație Anuală (%)",
            text="3",
            input_filter="float"
        )
        input_layout.add_widget(self.inflation_input)
        
        input_card.add_widget(input_layout)
        main_layout.add_widget(input_card)
        
        # Calculate Button
        calc_btn = MDButton(
            MDButtonIcon(icon="calculator"),
            MDButtonText(text="Calculează"),
            style="filled",
            size_hint_x=1,
            on_release=lambda x: self._calculate()
        )
        main_layout.add_widget(calc_btn)
        
        # Results
        results_row1 = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(95),
            spacing=dp(8)
        )
        
        self.stat_final = StatCard("Sold Final", "€ 0", "💰", (0.06, 0.73, 0.51, 1))
        self.stat_invested = StatCard("Total Investit", "€ 0", "📥", (0.23, 0.51, 0.96, 1))
        results_row1.add_widget(self.stat_final)
        results_row1.add_widget(self.stat_invested)
        main_layout.add_widget(results_row1)
        
        results_row2 = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(95),
            spacing=dp(8)
        )
        
        self.stat_profit = StatCard("Profit", "€ 0", "📈", (0.55, 0.36, 0.96, 1))
        self.stat_real = StatCard("Valoare Reală", "€ 0", "🎯", (0.96, 0.62, 0.04, 1))
        results_row2.add_widget(self.stat_profit)
        results_row2.add_widget(self.stat_real)
        main_layout.add_widget(results_row2)
        
        # Yearly breakdown - simplified list
        breakdown_card = MDCard(
            style="elevated",
            padding=dp(16),
            radius=dp(16),
            size_hint_y=None,
            height=dp(300)
        )
        
        breakdown_layout = MDBoxLayout(orientation='vertical')
        breakdown_layout.add_widget(MDLabel(
            text="📊 Evoluție Anuală",
            font_style="Title",
            role="medium",
            size_hint_y=None,
            height=dp(40)
        ))
        
        breakdown_scroll = MDScrollView()
        self.breakdown_list = MDList()
        breakdown_scroll.add_widget(self.breakdown_list)
        breakdown_layout.add_widget(breakdown_scroll)
        
        breakdown_card.add_widget(breakdown_layout)
        main_layout.add_widget(breakdown_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _calculate(self):
        try:
            capital = float(self.capital_input.text or 0)
            monthly = float(self.monthly_input.text or 0)
            years = int(self.years_input.text or 0)
            rate = float(self.rate_input.text or 0) / 100
            inflation = float(self.inflation_input.text or 0) / 100
            
            total = capital
            total_invested = capital
            
            self.breakdown_list.clear_widgets()
            
            for year in range(1, years + 1):
                deposit = monthly * 12
                total_invested += deposit
                interest = (total + deposit/2) * rate
                total = total + deposit + interest
                real_value = total / ((1 + inflation) ** year)
                
                item = MDListItem(
                    MDListItemHeadlineText(text=f"An {year}"),
                    MDListItemSupportingText(text=f"Sold: € {total:,.0f} | Real: € {real_value:,.0f}")
                )
                self.breakdown_list.add_widget(item)
            
            profit = total - total_invested
            final_real = total / ((1 + inflation) ** years)
            
            self.stat_final.set_value(f"€ {total:,.0f}")
            self.stat_invested.set_value(f"€ {total_invested:,.0f}")
            self.stat_profit.set_value(f"€ {profit:,.0f}")
            self.stat_real.set_value(f"€ {final_real:,.0f}")
            
        except Exception as e:
            print(f"Calculation error: {e}")
