from decimal import *


def precise_result(value):
    """Counts properly rounded result using Decimal module"""
    return str(Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
