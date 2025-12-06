"""
ManuX Wealth OS - Basket Screen (Coș Lunar România)
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivy.metrics import dp


class BasketScreen(MDScreen):
    """Romanian minimum consumption basket"""
    
    BASKET_DATA = {
        2024: {"1 Adult": 2847, "2 Adulți": 4523, "2+1 Copil": 5891, "2+2 Copii": 7156},
        2025: {"1 Adult": 3102, "2 Adulți": 4930, "2+1 Copil": 6421, "2+2 Copii": 7800}
    }
    EUR_RATE = 4.98
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_year = 2024
        self.selected_type = "1 Adult"
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="🛒 Coș Lunar România", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Explanation
        explain_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(120))
        explain_card.md_bg_color = (0.02, 0.31, 0.23, 1)
        explain_card.add_widget(MDLabel(
            text="Coșul minim de consum reprezintă cheltuielile lunare necesare pentru un trai decent, "
                 "calculat de INS. Include: alimente, locuință, transport, sănătate.",
            font_style="Body", role="medium"
        ))
        main_layout.add_widget(explain_card)
        
        # Year selector
        year_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(8))
        
        self.btn_2024 = MDButton(MDButtonText(text="2024"), style="filled", on_release=lambda x: self._select_year(2024))
        self.btn_2025 = MDButton(MDButtonText(text="2025"), style="outlined", on_release=lambda x: self._select_year(2025))
        year_box.add_widget(self.btn_2024)
        year_box.add_widget(self.btn_2025)
        main_layout.add_widget(year_box)
        
        # Family type buttons
        type_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(4))
        self.type_buttons = {}
        for ftype in ["1 Adult", "2 Adulți", "2+1 Copil", "2+2 Copii"]:
            btn = MDButton(
                MDButtonText(text=ftype.replace(" ", "\n")),
                style="filled" if ftype == self.selected_type else "outlined",
                size_hint_x=0.25,
                on_release=lambda x, t=ftype: self._select_type(t)
            )
            self.type_buttons[ftype] = btn
            type_box.add_widget(btn)
        main_layout.add_widget(type_box)
        
        # Results
        results_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), spacing=dp(8))
        
        self.ron_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_x=0.5)
        self.ron_card.md_bg_color = (0.06, 0.73, 0.51, 1)
        ron_layout = MDBoxLayout(orientation='vertical')
        ron_layout.add_widget(MDLabel(text="💰 Total Lunar", halign="center"))
        self.ron_label = MDLabel(text="2,847 lei", font_style="Headline", role="small", halign="center")
        ron_layout.add_widget(self.ron_label)
        self.ron_card.add_widget(ron_layout)
        
        self.eur_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_x=0.5)
        self.eur_card.md_bg_color = (0.23, 0.51, 0.96, 1)
        eur_layout = MDBoxLayout(orientation='vertical')
        eur_layout.add_widget(MDLabel(text="💶 EUR", halign="center"))
        self.eur_label = MDLabel(text="€ 572", font_style="Headline", role="small", halign="center")
        eur_layout.add_widget(self.eur_label)
        self.eur_card.add_widget(eur_layout)
        
        results_box.add_widget(self.ron_card)
        results_box.add_widget(self.eur_card)
        main_layout.add_widget(results_box)
        
        # Comparison table
        table_card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(250))
        table_layout = MDBoxLayout(orientation='vertical')
        table_layout.add_widget(MDLabel(text="📊 Comparație Tipuri", font_style="Title", role="medium", size_hint_y=None, height=dp(40)))
        
        table_scroll = MDScrollView()
        self.table_list = MDList()
        table_scroll.add_widget(self.table_list)
        table_layout.add_widget(table_scroll)
        
        table_card.add_widget(table_layout)
        main_layout.add_widget(table_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
        
        self._update_display()
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
    
    def _select_year(self, year):
        self.selected_year = year
        self.btn_2024.style = "filled" if year == 2024 else "outlined"
        self.btn_2025.style = "filled" if year == 2025 else "outlined"
        self._update_display()
    
    def _select_type(self, ftype):
        self.selected_type = ftype
        for t, btn in self.type_buttons.items():
            btn.style = "filled" if t == ftype else "outlined"
        self._update_display()
    
    def _update_display(self):
        data = self.BASKET_DATA[self.selected_year]
        ron = data.get(self.selected_type, 2847)
        eur = int(ron / self.EUR_RATE)
        
        self.ron_label.text = f"{ron:,} lei".replace(",", " ")
        self.eur_label.text = f"€ {eur:,}".replace(",", " ")
        
        self.table_list.clear_widgets()
        for ftype, value in data.items():
            eur_val = int(value / self.EUR_RATE)
            item = MDListItem(
                MDListItemHeadlineText(text=ftype),
                MDListItemSupportingText(text=f"{value:,} lei / € {eur_val}".replace(",", " "))
            )
            self.table_list.add_widget(item)
