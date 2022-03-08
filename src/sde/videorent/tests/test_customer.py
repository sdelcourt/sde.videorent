# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from sde.videorent.testing import IntegrationTestCase


class TestCustomer(IntegrationTestCase):
    """Test Customer content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        portal = self.layer['portal']
        self.customer_Andre = portal.customers.andre
        self.customer_Gerard = portal.customers.gerard

    def test_customer_title(self):
        """ Test Customer custom title."""
        self.assertEquals(
            self.customer_Andre.Title(),
            'Sanfrapper André (Namur) - Bonus points: 5'
        )
        self.assertEquals(
            self.customer_Gerard.Title(),
            'Mansoif Gérard (Liège) - Bonus points: 10'
        )

    def test_customer_summary(self):
        """ Test Customer custom title."""
        self.assertEquals(
            self.customer_Andre.summary,
            'Sanfrapper André (Namur)'
        )
        self.assertEquals(
            self.customer_Gerard.summary,
            'Mansoif Gérard (Liège)'
        )
