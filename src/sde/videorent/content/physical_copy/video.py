# -*- coding: utf-8 -*-

from plone import api
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.supermodel import model

from sde.videorent import _

from zope import schema
from zope.i18n import translate
from zope.interface import implementer


class IVideoCopy(model.Schema):
    """
    VideoCopy zope schema.
    """

    copy_reference = schema.TextLine(
        title=_(u'label_copy_reference', default=u'Copy reference'),
        required=True
    )



@implementer(IVideoCopy)
class VideoCopy(Item):
    """
    VideoCopy class
    """
