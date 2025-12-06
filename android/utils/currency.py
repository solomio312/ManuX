"""
Currency API using ECB (European Central Bank)
Free, no API key required, works on Android
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict


class CurrencyAPI:
    """Fetch exchange rates from European Central Bank"""
    
    ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    
    def __init__(self):
        self.rates = {"EUR": 1.0}
        self.last_update = None
    
    def get_rates(self) -> Dict[str, float]:
        """Fetch latest exchange rates from ECB
        
        Returns:
            Dict with currency codes as keys and rates as values
            All rates are relative to EUR (EUR = 1.0)
        """
        try:
            response = requests.get(self.ECB_URL, timeout=10)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # ECB XML namespace
            namespaces = {
                'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
                'eurofxref': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
            }
            
            self.rates = {"EUR": 1.0}
            
            # Find all Cube elements with currency attribute
            for cube in root.findall('.//eurofxref:Cube[@currency]', namespaces):
                currency = cube.get('currency')
                rate = float(cube.get('rate'))
                self.rates[currency] = rate
            
            return self.rates
            
        except Exception as e:
            print(f"Error fetching ECB rates: {e}")
            # Return default rates if API fails
            return {
                "EUR": 1.0,
                "USD": 1.05,
                "RON": 4.98,
                "GBP": 0.86,
                "CHF": 0.94,
                "CAD": 1.45,
                "JPY": 158.0
            }
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount between currencies
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Converted amount
        """
        if not self.rates:
            self.get_rates()
        
        # Convert to EUR first, then to target
        if from_currency == "EUR":
            eur_amount = amount
        else:
            eur_amount = amount / self.rates.get(from_currency, 1.0)
        
        if to_currency == "EUR":
            return eur_amount
        else:
            return eur_amount * self.rates.get(to_currency, 1.0)
    
    def get_rate(self, currency: str) -> float:
        """Get rate for a single currency (relative to EUR)"""
        if not self.rates:
            self.get_rates()
        return self.rates.get(currency, 1.0)
