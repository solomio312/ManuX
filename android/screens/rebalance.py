"""
ManuX Wealth OS - Rebalance Screen
Portfolio rebalancing calculator
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivy.metrics import dp


class RebalanceScreen(MDScreen):
    """Portfolio rebalancing calculator"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assets = [
            {"name": "VWCE (Acțiuni)", "current": 60000, "target": 60},
            {"name": "AGGH (Obligațiuni)", "current": 25000, "target": 30},
            {"name": "Cash", "current": 15000, "target": 10},
        ]
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="⚖️ Rebalansare", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Explanation
        explain_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(120))
        explain_card.md_bg_color = (0.58, 0.18, 0.37, 1)
        explain_card.add_widget(MDLabel(
            text="Rebalansarea înseamnă ajustarea portofoliului pentru a reveni la alocarea țintă.\n\n"
                 "Recomandată anual sau când deviația e > 5%.",
            font_style="Body", role="medium"
        ))
        main_layout.add_widget(explain_card)
        
        # Total portfolio
        self.total_input = MDTextField(mode="outlined", hint_text="Valoare Totală Portofoliu (€)", text="100000")
        main_layout.add_widget(self.total_input)
        
        # Calculate
        calc_btn = MDButton(MDButtonText(text="⚖️ Calculează Rebalansare"), style="filled", on_release=lambda x: self._calculate())
        main_layout.add_widget(calc_btn)
        
        # Assets table
        table_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(300))
        table_layout = MDBoxLayout(orientation='vertical')
        table_layout.add_widget(MDLabel(text="📊 Portofoliu", font_style="Title", role="medium", size_hint_y=None, height=dp(40)))
        
        table_scroll = MDScrollView()
        self.assets_list = MDList()
        table_scroll.add_widget(self.assets_list)
        table_layout.add_widget(table_scroll)
        
        table_card.add_widget(table_layout)
        main_layout.add_widget(table_card)
        
        # Summary
        self.summary_label = MDLabel(text="", halign="center", font_style="Body", role="medium")
        main_layout.add_widget(self.summary_label)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
        
        self._update_table()
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _calculate(self):
        try:
            total = float(self.total_input.text or 100000)
            actual_total = sum(a["current"] for a in self.assets)
            
            if actual_total != total and actual_total > 0:
                ratio = total / actual_total
                for asset in self.assets:
                    asset["current"] *= ratio
            
            self._update_table()
            
            total_target = sum(a["target"] for a in self.assets)
            if abs(total_target - 100) > 0.1:
                self.summary_label.text = f"⚠️ Ținte: {total_target:.0f}% (ar trebui 100%)"
                self.summary_label.theme_text_color = "Custom"
                self.summary_label.text_color = (0.96, 0.62, 0.04, 1)
            else:
                self.summary_label.text = f"✅ Portofoliu: € {total:,.0f} | Ținte: 100%"
                self.summary_label.text_color = (0.06, 0.73, 0.51, 1)
                
        except Exception as e:
            print(f"Error: {e}")
    
    def _update_table(self):
        self.assets_list.clear_widgets()
        total = sum(a["current"] for a in self.assets)
        
        for asset in self.assets:
            current_pct = (asset["current"] / total * 100) if total > 0 else 0
            target_pct = asset["target"]
            diff = current_pct - target_pct
            
            if diff > 1:
                action = f"Vinde {diff:.1f}%"
                color = (0.94, 0.27, 0.27, 1)
            elif diff < -1:
                action = f"Cumpără {-diff:.1f}%"
                color = (0.06, 0.73, 0.51, 1)
            else:
                action = "OK ✓"
                color = (0.06, 0.73, 0.51, 1)
            
            item = MDListItem(
                MDListItemHeadlineText(text=asset["name"]),
                MDListItemSupportingText(text=f"Actual: {current_pct:.0f}% | Țintă: {target_pct}% → {action}")
            )
            self.assets_list.add_widget(item)
