# -*- coding: utf-8 -*-

from plone import api

from sde.videorent import _
from sde.videorent.config import RELEASE_TYPES

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ReleaseTypesVocabulary(object):
    """
    Vocabulary listing all the film release types.
    """

    def __call__(self, context):
        terms = [SimpleTerm(r_type, r_type, _(r_type)) for r_type in RELEASE_TYPES]
        vocabulary = SimpleVocabulary(terms)
        return vocabulary


ReleaseTypesVocabularyFactory = ReleaseTypesVocabulary()


class PhysicalSupportTypeVocabulary(object):
    """
    Vocabulary listing all the film release types.
    """

    def __call__(self, context):
        support_types = [
            'DVD',
            'Blueray',
            'HD_DVD',
            'VHS',
        ]
        terms = [SimpleTerm(s_type, s_type, _(s_type)) for s_type in support_types]
        vocabulary = SimpleVocabulary(terms)
        return vocabulary


PhysicalSupportTypeVocabularyFactory = PhysicalSupportTypeVocabulary()


class VideoCopiesVocabulary(object):
    """
    Vocabulary listing all the film copies.
    """

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='VideoCopy')
        terms = [SimpleTerm('', '', _('Choose'))]
        for brain in brains:
            terms.append(SimpleTerm(brain.UID, brain.UID, brain.Title))
        vocabulary = SimpleVocabulary(terms)
        return vocabulary


VideoCopiesVocabularyFactory = VideoCopiesVocabulary()
