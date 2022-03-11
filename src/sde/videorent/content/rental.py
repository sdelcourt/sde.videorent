# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow

from plone import api
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.supermodel import model


from sde.videorent import _
from sde.videorent.config import BONUS_BY_RELEASE_TYPES
from sde.videorent.config import FEES_FORMULAS
from sde.videorent.config import PRICES_FORMULAS

from zope import schema
from zope.interface import implementer

import datetime


class IRentedRowSchema(model.Schema):
    """
    Row schema for datagridfield 'rented'.
    """
    video_copy = schema.Choice(
        title=_(u'label_film', default=u'Film'),
        vocabulary='videorent.vocabularies.video_copies',
        required=True,
    )

    duration = schema.Int(
        title=_(u'label_duration', default=u'Duration'),
        default=3,
        required=True,
    )

    returned = schema.Bool(
        title=_(u'label_returned', default=u'Returned'),
        default=False,
    )


class ILateFeesRowSchema(model.Schema):
    """
    Row schema for datagridfield 'late_fees'.
    """
    video_copy = schema.Choice(
        title=_(u'label_film', default=u'Film'),
        vocabulary='videorent.vocabularies.video_copies',
        readonly=True,
    )

    late_days = schema.Int(
        title=_(u'label_late_days', default=u'Late days'),
        readonly=True,
    )

    fee = schema.Int(
        title=_(u'label_fee', default=u'Fee'),
        readonly=True,
    )


class IRental(model.Schema):
    """
    Rental zope schema.
    """

    directives.widget('customer', AutocompleteFieldWidget)
    customer = schema.Choice(
        title=_(u'label_customer', default=u'Customer'),
        source=UUIDSourceBinder(portal_type='Customer'),
        required=True,
    )

    start_date = schema.Date(
        title=_(u'label_start_date', default=u'Start date'),
        default=datetime.date.today(),
        required=True
    )

    directives.widget('rented', DataGridField)
    rented = schema.List(
        title=_(u'label_rented', default=u'Rented'),
        value_type=DictRow(title=u"tablerow", schema=IRentedRowSchema),
        required=True,
    )

    price = schema.Int(
        title=_(u'label_price', default=u'Price'),
        readonly=True,
    )

    bonus_points = schema.Int(
        title=_(u'label_bonus_points', default=u'Bonus points'),
        readonly=True,
    )

    directives.widget('late_fees', DataGridField)
    late_fees = schema.List(
        title=_(u'label_late_fees', default=u'Late fees'),
        value_type=DictRow(title=u"tablerow", schema=ILateFeesRowSchema),
        readonly=True,
    )

    total_fees = schema.Int(
        title=_(u'label_total_fees', default=u'Total fees'),
        readonly=True,
    )


@implementer(IRental)
class Rental(Item):
    """
    Rental class
    """

    def Title(self):
        """
        Customise Title.
        """
        customer = self.get_customer()
        title = '{} - {}'.format(
            self.start_date.strftime('%d/%m/%Y'),
            customer and customer.summary or '',
        )
        return title

    def get_customer(self):
        """
        customer field getter.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=self.customer)
        if brains:
            customer = brains[0].getObject()
            return customer

    def get_video_copies_late_fees(self, video_copies):
        """
        Return the late fees of video_copies if they exist.
        """
        late_fees = []
        for line in self.late_fees:
            if line['video_copy'] in video_copies:
                late_fees.append(line)
        return late_fees

    def set_returned_video_copies(self, video_copies):
        """
        Set the attribute 'returned' to True in field rental for each VideoCopies.
        """
        for line in self.rented:
            if line['video_copy'] in video_copies:
                line['returned'] = True

    @property
    def bonus_points(self):
        """
        Compute bonus points of the rental.
        """
        total_bonus = 0
        for video_copy in self._search_video_copies():
            release_type = video_copy.get_film().release_type
            total_bonus += BONUS_BY_RELEASE_TYPES[release_type]
        return total_bonus

    @property
    def price(self):
        """
        Compute total renting price.
        """
        total_price = 0
        for rent in self.rented:
            video_copy = self._search_video_copy(rent['video_copy'])
            release_type = video_copy.get_film().release_type
            formula = PRICES_FORMULAS[release_type]
            total_price += formula(rent['duration'])
        return total_price

    @property
    def late_fees(self):
        """
        Compute a read only datagrid with late fees informations.
        """
        late_fees = []
        for rent in self.rented:
            late_days = max(0, (datetime.date.today() - self.start_date).days - rent['duration'])
            if late_days and not rent['returned']:
                video_copy = self._search_video_copy(rent['video_copy'])
                release_type = video_copy.get_film().release_type
                fee_formula = FEES_FORMULAS[release_type]
                fee = fee_formula(late_days)
                late_fees.append(
                    {
                        'video_copy': rent['video_copy'],
                        'late_days': late_days,
                        'fee': fee,
                    }
                )
        return late_fees

    @property
    def total_fees(self):
        """
        Compute total fees price.
        """
        total_fees = sum([fee['fee'] for fee in self.late_fees or []])
        return total_fees

    def _search_video_copy(self, copy_UID):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=copy_UID)
        if brains:
            video_copy = brains[0].getObject()
            return video_copy

    def _search_video_copies(self):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=[r['video_copy'] for r in self.rented])
        video_copies = [brain.getObject() for brain in brains]
        return video_copies
