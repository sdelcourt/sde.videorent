# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from sde.videorent.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of sde.videorent into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if sde.videorent is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('sde.videorent'))

    def test_application_folders(self):
        """
        Test if application folders are created correctly.
        """
        expected_result = [
            {'id': 'rentals', 'title': 'Locations', 'allowed_types': ('Rental',)},
            {'id': 'films',  'title': 'Fiches film', 'allowed_types': ('Film',)},
            {'id': 'copies',  'title': 'Exemplaires', 'allowed_types': ('VideoCopy',)},
            {'id': 'customers',  'title': 'Clients', 'allowed_types': ('Customer',)},
        ]
        app_folders = self.portal.objectValues('ATFolder')
        self.assertEquals(len(app_folders), 4)
        for index, folder in enumerate(app_folders):
            expected = expected_result[index]
            self.assertEquals(folder.id, expected['id'])
            self.assertEquals(folder.Title(), expected['title'])
            self.assertEquals(folder.immediatelyAddableTypes, expected['allowed_types'])

    def test_uninstall(self):
        """Test if sde.videorent is cleanly uninstalled."""
        self.installer.uninstallProducts(['sde.videorent'])
        self.assertFalse(self.installer.isProductInstalled('sde.videorent'))
