import random

from .models import Promo

CHARS = '0123456789QWERTYUIOPASDFGHJKLZXCVBNM'

def generate_promo():
    length = 6
    while True:
        code = ''.join(random.choices(CHARS, k=length))
        if Promo.objects.filter(promocode=code).count() == 0:
            break
    return code