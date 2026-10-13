from trytond.pool import PoolMeta
import requests

class CurrencyBcvUpdate(metaclass=PoolMeta):
    __name__ = 'currency.cron'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        new_source = ('bcv', 'Banco Central de Venezuela (BCV)')
        if new_source not in cls.source.selection:
            cls.source.selection = list(cls.source.selection) + [new_source]

    @classmethod
    def update_rates(cls, records=None):
        if records is None:
            records = cls.search([])

        bcv_records = [u for u in records if u.source == 'bcv']
        other_records = [u for u in records if u.source != 'bcv']

        if other_records:
            super().update_rates(records=other_records)

        if records:
            for record in bcv_records:
                cls._update_rates_bcv(record)

    @classmethod
    def _update_rates_bcv(cls, record):
        response = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=20) # api endpoint for BCV rates, solo para el dolar oficial
        if response.status_code == 200:
            print("BCV API response:", response.json())