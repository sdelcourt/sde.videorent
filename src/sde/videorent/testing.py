# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

from sde.videorent.profiles.testing.mock_data import TEST_USER_NAME

import unittest

import sde.videorent


class SdeVideorentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = (
        'sde.videorent',
        'collective.z3cform.datagridfield',
    )

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=sde.videorent,
                      name='testing.zcml')
        for p in self.products:
            z2.installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Set language to 'fr'
        ltool = portal.portal_languages
        defaultLanguage = 'fr'
        supportedLanguages = ['en', 'fr']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages,
                                         setUseCombinedLanguageCodes=False)
        portal.portal_languages.setLanguageBindings()

        # Install into Plone site using portal_setup
        applyProfile(portal, 'sde.videorent:testing')

        # Login
        login(portal, TEST_USER_NAME)

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


FIXTURE = SdeVideorentLayer(
    name="FIXTURE"
    )


INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION"
    )


FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE, z2.ZSERVER_FIXTURE),
    name="FUNCTIONAL"
    )


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL
