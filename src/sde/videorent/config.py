# -*- coding: utf-8 -*-

RELEASE_TYPES = [
    'new',
    'regular',
    'old'
]

BONUS_BY_RELEASE_TYPES = {
    'new': 2,
    'regular': 1,
    'old': 1
}

PRICE = {
    'basic': 3,
    'premium': 4,
}

PRICES_FORMULAS = {
    'new': lambda duration: duration * PRICE['premium'],
    'regular': lambda duration: PRICE['basic'] + max(0, duration - 3) * PRICE['basic'],
    'old': lambda duration: PRICE['basic'] + max(0, duration - 5) * PRICE['basic'],
}

FEES_FORMULAS = {
    'new': lambda late_days: late_days * PRICE['premium'],
    'regular': lambda late_days: late_days * PRICE['basic'],
    'old': lambda late_days: late_days * PRICE['basic'],
}
