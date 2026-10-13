from trytond.pool import Pool
from . import bcv

def register():
    Pool.register(
        bcv.CurrencyBcvUpdate,
        module='rate_bcv', 
        type_='model'
    )