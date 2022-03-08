# -*- coding: utf-8 -*-

from sde.videorent import _

from plone.dexterity.content import Item
from plone.supermodel import model

from zope import schema
from zope.i18n import translate
from zope.interface import implementer


class ICustomer(model.Schema):
    """
    Customer zope schema.
    """

    name = schema.TextLine(
        title=_(u'label_name', default=u'Name'),
        required=True
    )

    firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'Firstname'),
        required=True
    )

    bonus_points = schema.Int(
        title=_(u'label_bonus_points', default=u'Bonus points'),
        default=0,
        required=True
    )

    address = schema.TextLine(
        title=_(u'label_address', default=u'Address'),
        required=True
    )

    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        required=True
    )

    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Phone'),
        required=False
    )

    email = schema.TextLine(
        title=_(u'label_email', default=u'E-mail'),
        required=False
    )


@implementer(ICustomer)
class Customer(Item):
    """
    Customer class
    """

    def Title(self):
        title = '{} - {}: {}'.format(
            self.summary,
            translate(_(u'label_bonus_points', default='Bonus points'), context=self.REQUEST),
            str(self.bonus_points),
        )
        return title

    @property
    def summary(self):
        summary = '{} {} ({})'.format(
            self.name,
            self.firstname,
            self.city,
        )
        return summary
