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

    def test_uninstall(self):
        """Test if sde.videorent is cleanly uninstalled."""
        self.installer.uninstallProducts(['sde.videorent'])
        self.assertFalse(self.installer.isProductInstalled('sde.videorent'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ISdeVideorentLayer is registered."""
        from sde.videorent.interfaces import ISdeVideorentLayer
        from plone.browserlayer import utils
        self.assertIn(ISdeVideorentLayer, utils.registered_layers())
