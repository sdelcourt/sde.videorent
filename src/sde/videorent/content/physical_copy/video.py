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

    directives.widget('film', AutocompleteFieldWidget)
    film = schema.Choice(
        title=_(u'label_film', default=u'Film'),
        source=UUIDSourceBinder(portal_type='Film'),
        required=True,
    )

    physical_support = schema.Choice(
        title=_(u'label_release_type', default='Release type'),
        vocabulary='videorent.vocabularies.physical_supports',
        required=True,
        default='DVD',
    )


@implementer(IVideoCopy)
class VideoCopy(Item):
    """
    VideoCopy class
    """

    def Title(self):
        film = self.get_film()
        title = u'{} ({} {}) - {}'.format(
            film and film.Title() or '',
            self.physical_support,
            film and translate(_(film.release_type), context=self.REQUEST) or '',
            self.copy_reference,
        )
        return title.encode('utf-8')

    def get_film(self):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=hasattr(self, 'film') and self.film or None)
        if brains:
            film = brains[0].getObject()
            return film
