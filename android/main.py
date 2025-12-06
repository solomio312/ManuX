"""
ManuX Wealth OS - Android Version
Main entry point using KivyMD for Material Design UI
"""

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from screens.home import HomeScreen
from screens.calculator import CalculatorScreen
from screens.monte_carlo import MonteCarloScreen
from screens.basket import BasketScreen
from screens.fire import FireScreen
from screens.real_estate import RealEstateScreen
from screens.rebalance import RebalanceScreen
from screens.tax import TaxScreen
from screens.guide import GuideScreen
from utils.currency import CurrencyAPI


class ManuXWealthOS(MDApp):
    """Main Application Class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.currency_api = CurrencyAPI()
        self.currency = "EUR"
        self.exchange_rates = {"EUR": 1.0, "USD": 1.05, "RON": 4.98, "CAD": 1.45, "GBP": 0.86}
    
    def build(self):
        # Theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.material_style = "M3"
        
        # Screen Manager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CalculatorScreen(name='calculator'))
        self.sm.add_widget(MonteCarloScreen(name='monte_carlo'))
        self.sm.add_widget(BasketScreen(name='basket'))
        self.sm.add_widget(FireScreen(name='fire'))
        self.sm.add_widget(RealEstateScreen(name='real_estate'))
        self.sm.add_widget(RebalanceScreen(name='rebalance'))
        self.sm.add_widget(TaxScreen(name='tax'))
        self.sm.add_widget(GuideScreen(name='guide'))
        
        return self.sm
    
    def go_home(self):
        """Navigate to home screen"""
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'
    
    def go_to(self, screen_name):
        """Navigate to a screen"""
        self.sm.transition.direction = 'left'
        self.sm.current = screen_name
    
    def refresh_rates(self):
        """Refresh exchange rates from ECB"""
        try:
            self.exchange_rates = self.currency_api.get_rates()
            return True
        except:
            return False


if __name__ == '__main__':
    ManuXWealthOS().run()
