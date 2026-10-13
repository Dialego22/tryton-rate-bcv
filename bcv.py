from trytond.model import PoolMeta, fields

class CurrencyBcvUpdate(metaclass=PoolMeta):
    __name__ = 'currency.scheduled_update'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        new_source = ('banco_central_ve', 'Banco Central de Venezuela (BCV)')
        if new_source not in cls.source.selection:
            cls.source.selection.append(new_source)

    @classmethod
    def update_rates(cls, updates=None):
        super().update_rates(updates=updates)
        cls._update_rates_bcv()
        if updates:
            for update in updates:
                if update.source == 'banco_central_ve':
                    cls._actualizar_con_mi_api(update)

    @classmethod
    def _update_rates_bcv(cls):
        import requests
        response = requests.get("https://ve.dolarapi.com/v1/dolares/oficial") # api endpoint for BCV rates, solo para el dolar oficial
        if response.status_code == 200:
            print("BCV API response:", response.json())