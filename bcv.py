from trytond.pool import PoolMeta
from decimal import Decimal
import requests

class CurrencyBcvUpdate(metaclass=PoolMeta):
    __name__ = 'currency.cron'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        new_source = ('bcv', 'Banco Central de Venezuela (BCV)')
        if new_source not in cls.source.selection:
            cls.source.selection = list(cls.source.selection) + [new_source]

    def fetch_bcv(self, date_):
        try:
            response = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=20) # api endpoint for BCV rates, solo para el dolar oficial
            if response.status_code == 200:
                data = response.json()
                rate = round(Decimal(str(data['promedio'])), 5)
                return {
                    'VES': rate
                }
        except requests.RequestException as e:
            print(f"Error fetching BCV rates: {e}")
        return {}
