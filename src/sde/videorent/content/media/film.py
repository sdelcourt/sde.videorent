# -*- coding: utf-8 -*-

from sde.videorent import _

from plone.dexterity.content import Item
from plone.supermodel import model

from zope import schema
from zope.interface import implementer


class IFilm(model.Schema):
    """
    Film zope schema.
    """

    release_type = schema.Choice(
        title=_(u'label_release_type', default='Release type'),
        vocabulary='videorent.vocabularies.release_types',
        required=True,
        default='regular',
    )


@implementer(IFilm)
class Film(Item):
    """
    Film class
    """
