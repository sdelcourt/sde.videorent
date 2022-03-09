# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from sde.videorent.testing import IntegrationTestCase


class TestIndexes(IntegrationTestCase):
    """Test installation of sde.videorent into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.catalog = self.portal.portal_catalog

    def test_rented_video_copies_index(self):
        """
        Test if rented_video_copies returns the rental containing the video copies
        who are still not returned.
        """
        video_copies = self.portal.copies

        # search on non rented VideoCopies
        brains = self.catalog(rented_video_copies=[video_copies.c2.UID(), video_copies.c6.UID()])
        self.assertEquals(len(brains), 0)

        # search on rented VideoCopies
        brains = self.catalog(rented_video_copies=[video_copies.c1.UID(), video_copies.c4.UID()])
        rental = self.portal.rentals.rental
        self.assertEquals(len(brains), 1)
        self.assertEquals(brains[0].getObject(), rental)

        # if we return VideoCopy c1 and c4, we wont find the rental anymore
        rental.rented[0]['returned'] = True
        rental.rented[2]['returned'] = True
        rental.reindexObject()
        brains = self.catalog(rented_video_copies=[video_copies.c1.UID(), video_copies.c4.UID()])
        self.assertEquals(len(brains), 0)
