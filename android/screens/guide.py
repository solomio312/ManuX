"""
ManuX Wealth OS - Guide Screen
Investment education guide
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelHeader, MDExpansionPanelContent
from kivy.metrics import dp


class GuideScreen(MDScreen):
    """Investment education guide"""
    
    GUIDES = [
        ("📊", "Ce sunt ETF-urile?", 
         "ETF = Exchange-Traded Fund\n\nAvantaje:\n• Diversificare instantanee\n• Costuri reduse (0.1-0.5%/an)\n• Lichiditate mare\n\nPopulare: VWCE, IWDA, AGGH"),
        
        ("💹", "Dobânda Compusă",
         "Formula: A = P × (1 + r)^n\n\nExemplu la 7%/an:\n• 10,000€ → 10 ani: 19,672€\n• 10,000€ → 20 ani: 38,697€\n• 10,000€ → 30 ani: 76,123€\n\nRegula 72: ani = 72 / rata%"),
        
        ("📉", "Dollar-Cost Averaging",
         "DCA = Investiții regulate, indiferent de preț.\n\nAvantaje:\n• Elimină stresul timing\n• Reduce impactul volatilității\n• Creează disciplină\n• Funcționează automat"),
        
        ("🎯", "Diversificare",
         "Nu pune toate ouăle în același coș.\n\nAlocări clasice:\n• Agresiv (20-30 ani): 90/10\n• Moderat (30-50 ani): 70/30\n• Conservator (>50 ani): 50/50\n\nRegula: % acțiuni = 110 - vârsta"),
        
        ("🔥", "Mișcarea FIRE",
         "FIRE = Financial Independence, Retire Early\n\nVariante:\n• Fat FIRE: Stil luxos\n• Lean FIRE: Viață frugală\n• Barista FIRE: Job part-time\n• Coast FIRE: Las compunerea să lucreze"),
        
        ("⚠️", "Gestionarea Riscurilor",
         "Tipuri de risc:\n• Risc de piață (30-50% scădere)\n• Risc de inflație\n• Risc valutar\n\nFond de Urgență:\n• 3-6 luni cheltuieli\n• ÎNAINTE de investiții"),
        
        ("❌", "Greșeli Comune",
         "1. Timing-ul pieței\n2. Panică în criză\n3. Urmărirea performanțelor trecute\n4. Supradiversificare\n5. Ignorarea costurilor\n6. Trading frecvent"),
        
        ("🛠️", "Brokeri Recomandați",
         "Interactive Brokers: Cel mai serios\nXTB: Fără comisioane\nDEGIRO: Costuri mici\nTrading 212: Fractional shares\n\nAplicații: JustETF, Portfolio Performance"),
        
        ("🧠", "Psihologia Investitorului",
         "Biasuri cognitive:\n• Loss Aversion\n• Confirmation Bias\n• Recency Bias\n• Herd Mentality\n\nSfat: Scrie strategia ÎNAINTE de criză"),
        
        ("🚀", "Plan de Acțiune",
         "Săptămâna 1:\n□ Deschide cont broker\n□ Fond de urgență\n□ Calculează bugetul\n\nLunar:\n□ Investiție automată (DCA)\n□ NU verifica zilnic\n\nCel mai bun moment e ACUM!"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        scroll = MDScrollView()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(8), adaptive_height=True)
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self._go_back()))
        header.add_widget(MDLabel(text="📚 Ghid Investiții", font_style="Headline", role="small"))
        main_layout.add_widget(header)
        
        # Subtitle
        main_layout.add_widget(MDLabel(
            text="Educație financiară pentru începători",
            font_style="Body", role="medium",
            theme_text_color="Secondary",
            size_hint_y=None, height=dp(30)
        ))
        
        # Guide cards
        for icon, title, content in self.GUIDES:
            card = MDCard(style="elevated", padding=dp(16), radius=dp(16), size_hint_y=None, height=dp(200))
            card.md_bg_color = (0.36, 0.13, 0.53, 1)
            
            card_layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
            card_layout.add_widget(MDLabel(
                text=f"{icon} {title}",
                font_style="Title", role="medium",
                size_hint_y=None, height=dp(30)
            ))
            card_layout.add_widget(MDLabel(
                text=content,
                font_style="Body", role="small"
            ))
            
            card.add_widget(card_layout)
            main_layout.add_widget(card)
        
        # Footer
        main_layout.add_widget(MDLabel(
            text="⚠️ Acest ghid nu constituie sfat financiar.",
            font_style="Body", role="small",
            theme_text_color="Custom",
            text_color=(0.96, 0.62, 0.04, 1),
            halign="center",
            size_hint_y=None, height=dp(40)
        ))
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def _go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_home()
