# -*- coding: utf-8 -*-

from sde.videorent import config
from sde.videorent.testing import IntegrationTestCase

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabularies(IntegrationTestCase):
    """Test vocabularies of sde.videorent."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_release_types_vocabulary(self):
        """Test release types vocabulary."""
        voc_titles, voc_values = self._get_vocabulary('videorent.vocabularies.release_types')
        self.assertEquals(voc_titles, config.RELEASE_TYPES)
        self.assertEquals(voc_values, config.RELEASE_TYPES)

    def test_support_types_vocabulary(self):
        """Test physical support types vocabulary."""
        voc_titles, voc_values = self._get_vocabulary('videorent.vocabularies.physical_supports')
        expected_support_types = ['DVD', 'Blueray', 'HD_DVD', 'VHS']
        self.assertEquals(voc_titles, expected_support_types)
        self.assertEquals(voc_values, expected_support_types)

    def test_video_copies_vocabulary(self):
        """Test VideoCopy vocabulary."""
        voc_titles, voc_values = self._get_vocabulary('videorent.vocabularies.video_copies')
        video_copies = self.portal.copies.objectValues()
        expected_values = [''] + [copy.UID() for copy in video_copies]
        self.assertEquals(voc_values, expected_values)

    def _get_vocabulary(self, voc_name):
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.portal)
        voc_titles = [t.title for t in vocabulary]
        voc_values = [t.value for t in vocabulary]
        return voc_titles, voc_values
