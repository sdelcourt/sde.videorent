# -*- coding: utf-8 -*-


def update_customer_bonus_points(rental, event):
    """
    When creating a new rental, update the customer bonus points
    accordingly.
    """
    customer = rental.get_customer()
    if customer:
        customer.bonus_points += rental.bonus_points
        customer.reindexObject()
