"""
ManuX Wealth OS - Home Screen
Main navigation with elegant Material Design buttons
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp


class ModuleCard(MDCard):
    """Elegant card button for module navigation"""
    
    def __init__(self, icon, title, description, color, screen_name, **kwargs):
        super().__init__(**kwargs)
        self.screen_name = screen_name
        self.style = "elevated"
        self.size_hint = (None, None)
        self.size = (dp(160), dp(140))
        self.padding = dp(16)
        self.radius = dp(16)
        self.ripple_behavior = True
        self.md_bg_color = color
        
        # Layout
        layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
        
        # Icon
        icon_label = MDLabel(
            text=icon,
            font_style="Display",
            role="small",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(icon_label)
        
        # Title
        title_label = MDLabel(
            text=title,
            font_style="Title",
            role="medium",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)
        
        # Description
        desc_label = MDLabel(
            text=description,
            font_style="Body",
            role="small",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8)
        )
        layout.add_widget(desc_label)
        
        self.add_widget(layout)
        self.bind(on_release=self.navigate)
    
    def navigate(self, *args):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_to(self.screen_name)


class HomeScreen(MDScreen):
    """Main home screen with navigation buttons"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.backgroundColor if hasattr(self, 'theme_cls') else (0.06, 0.09, 0.16, 1)
        self._build_ui()
    
    def _build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(16)
        )
        
        # Header
        header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(12)
        )
        
        # Logo
        try:
            logo = FitImage(source='assets/logo.png', size_hint=(None, None), size=(dp(60), dp(60)))
            header.add_widget(logo)
        except:
            pass
        
        # Title
        title_box = MDBoxLayout(orientation='vertical')
        title_box.add_widget(MDLabel(
            text="ManuX Wealth OS",
            font_style="Headline",
            role="small",
            theme_text_color="Primary"
        ))
        title_box.add_widget(MDLabel(
            text="Enterprise 16.2",
            font_style="Body",
            role="medium",
            theme_text_color="Secondary"
        ))
        header.add_widget(title_box)
        
        main_layout.add_widget(header)
        
        # Subtitle
        main_layout.add_widget(MDLabel(
            text="Simulator avansat pentru proiecții financiare",
            font_style="Body",
            role="large",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        ))
        
        # Modules Grid
        modules_grid = MDGridLayout(
            cols=2,
            spacing=dp(16),
            padding=dp(8),
            adaptive_height=True
        )
        
        # Module cards with colors matching desktop
        modules = [
            ("🧮", "Calculator", "Proiecție investiții", (0.23, 0.51, 0.96, 1), "calculator"),
            ("🎲", "Monte Carlo", "Simulare 10K scenarii", (0.55, 0.36, 0.96, 1), "monte_carlo"),
            ("🛒", "Coș Lunar", "Cheltuieli minime RO", (0.06, 0.73, 0.51, 1), "basket"),
            ("🔥", "FIRE", "Simulator pensie", (0.96, 0.62, 0.04, 1), "fire"),
            ("🏠", "Imobiliar", "Calculator ROI", (0.02, 0.71, 0.83, 1), "real_estate"),
            ("⚖️", "Rebalansare", "Ajustare portofoliu", (0.93, 0.29, 0.60, 1), "rebalance"),
            ("💸", "Taxe", "RO / CA / US", (0.94, 0.27, 0.27, 1), "tax"),
            ("📚", "Ghid", "Educație financiară", (0.98, 0.75, 0.14, 1), "guide"),
        ]
        
        for icon, title, desc, color, screen in modules:
            card = ModuleCard(icon, title, desc, color, screen)
            modules_grid.add_widget(card)
        
        main_layout.add_widget(modules_grid)
        
        # Footer - Currency info
        footer = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )
        
        self.rate_label = MDLabel(
            text="1 EUR = 4.98 RON | 1 USD = 1.05 EUR",
            font_style="Body",
            role="small",
            theme_text_color="Secondary",
            halign="center"
        )
        footer.add_widget(self.rate_label)
        
        main_layout.add_widget(footer)
        
        self.add_widget(main_layout)
