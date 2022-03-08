# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from sde.videorent.testing import IntegrationTestCase


class TestVideoCopy(IntegrationTestCase):
    """Test Film content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        portal = self.layer['portal']
        self.copies = portal.copies
        self.films = portal.films

    def test_videocopy_title(self):
        """ Test VideoCopy custom title."""

        self.assertEquals(
            self.copies.c1.Title(),
            'MATRIX 11 (HD_DVD new) - SF0045'
        )
        self.assertEquals(
            self.copies.c3.Title(),
            'Spiderman (DVD regular) - MVL0096'
        )

    def test_videocopy_get_film(self):
        """ Test VideoCopy get_film method."""

        matrix_film = self.films.matrix_11
        self.assertEquals(self.copies.c1.get_film(), matrix_film)
        self.assertEquals(self.copies.c2.get_film(), matrix_film)

        africa_film = self.films.out_of_africa
        self.assertEquals(self.copies.c5.get_film(), africa_film)
        self.assertEquals(self.copies.c6.get_film(), africa_film)
