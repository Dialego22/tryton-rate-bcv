from trytond.pool import Pool, PoolMeta
from datetime import datetime, date
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
        response = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=20) # api endpoint for BCV rates, solo para el dolar oficial
        if response.status_code == 200:
            data = response.json()

            Rate = Pool().get('currency.currency.rate')

            for currency in self.currencies:
                at_currency = datetime.fromisoformat(data['fechaActualizacion']).date()
                Rate.create([{
                    'currency': currency.id,
                    'rate': round(float(data['promedio']), 5),
                    'date': at_currency,
                }])
            
