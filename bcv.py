from trytond.model import PoolMeta
import requests

class CurrencyBcvUpdate(metaclass=PoolMeta):
    __name__ = 'currency.scheduled_update'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        new_source = ('banco_central_ve', 'Banco Central de Venezuela (BCV)')
        if new_source not in cls.source.selection:
            cls.source.selection = list(cls.source.selection) + [new_source]

    @classmethod
    def update_rates(cls, updates=None):
        if updates is None:
            updates = cls.search([])

        bcv_updates = [u for u in updates if u.source == 'banco_central_ve']
        other_updates = [u for u in updates if u.source != 'banco_central_ve']

        if other_updates:
            super().update_rates(updates=other_updates)

        if bcv_updates:
            cls._update_rates_bcv(bcv_updates)

    @classmethod
    def _update_rates_bcv(cls):
        response = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=20) # api endpoint for BCV rates, solo para el dolar oficial
        if response.status_code == 200:
            print("BCV API response:", response.json())