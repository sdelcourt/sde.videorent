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


class IRental(model.Schema):
    """
    Rental zope schema.
    """


@implementer(IRental)
class Rental(Item):
    """
    Rental class
    """

