from trytond.pool import Pool
from . import bcv

def register():
    Pool.register(
        bcv.BCV,
        module='rate_bcv', type_='model'
    )