from trytond.model import PoolMeta

class CurrencyBcvUpdate(metaclass=PoolMeta):
    __name__ = 'currency.scheduled_update'

    @classmethod
    def update_rates(cls, updates=None):
        
        cls._update_rates_bcv()

    @classmethod
    def _update_rates_bcv(cls):
        print("¡La tarea automática de tasas se ejecutó con mi propio código!")
