# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from datetime import date
from datetime import timedelta

from sde.videorent.testing import FunctionalTestCase


class TestRental(FunctionalTestCase):
    """Test Rental content type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        portal = self.layer['portal']
        self.copies = portal.copies
        self.films = portal.films
        self.customers = portal.customers
        self.rental = portal.rentals.rental

    def test_rental_title(self):
        """ Test Rental custom title."""
        self.assertEquals(
            self.rental.Title(),
            '{} - Sanfrapper André (Namur)'.format(date.today().strftime('%d/%m/%Y'))
        )

    def test_rental_get_customer(self):
        """ Test Rental get_customer method."""
        self.assertEquals(self.rental.get_customer(), self.customers.andre)

    def test_rental_get_video_copies_late_fees(self):
        """ Test Rental get_video_copies_late_fees method."""
        video_copies = [self.copies.c1.UID(), self.copies.c3.UID()]
        rental = self.rental

        # so far nothing is late
        self.assertEquals(rental.get_video_copies_late_fees(video_copies), [])

        # set -4 days to the start date so the VideoCopy c1 is late
        rental.start_date = rental.start_date - timedelta(days=4)
        late_fees = rental.get_video_copies_late_fees(video_copies)
        self.assertEquals(len(late_fees), 1)
        c1_late_fee = rental.get_video_copies_late_fees(video_copies)[0]

        # now VideoCopy c1 is late by 3 days
        self.assertEquals(c1_late_fee['late_days'], 3)
        # and has 12 euros fee (3 days * premium price 4 euros)
        self.assertEquals(c1_late_fee['fee'], 12)

        # set -7 days to the start date so both VideoCopies c1 and c2 are late
        rental.start_date = rental.start_date - timedelta(days=3)
        late_fees = rental.get_video_copies_late_fees(video_copies)
        self.assertEquals(len(late_fees), 2)
        c1_late_fee = rental.get_video_copies_late_fees(video_copies)[0]
        c2_late_fee = rental.get_video_copies_late_fees(video_copies)[1]

        # now VideoCopy c1 is late by 6 days
        self.assertEquals(c1_late_fee['late_days'], 6)
        # and has 24 euros fee (6 days * premium price 4 euros)
        self.assertEquals(c1_late_fee['fee'], 24)
        # now VideoCopy c2 is late by 2 days
        self.assertEquals(c2_late_fee['late_days'], 2)
        # and has 3 euros fee (2 days * basic price 6 euros)
        self.assertEquals(c2_late_fee['fee'], 6)

        # return VideoCopy c1, now c1 should not be included in the late fees anymore.
        rental.set_returned_video_copies([self.copies.c1.UID()])
        late_fees = rental.get_video_copies_late_fees(video_copies)
        # we only have one late fee info: c2
        self.assertEquals(len(late_fees), 1)
        c2_late_fee = rental.get_video_copies_late_fees(video_copies)[0]
        # c2 late fees are still the same
        self.assertEquals(c2_late_fee['late_days'], 2)
        self.assertEquals(c2_late_fee['fee'], 6)

    def test_rental_set_returned_video_copies(self):
        """ Test Rental set_returned_video_copies method."""
        video_copies = [self.copies.c1.UID(), self.copies.c3.UID()]
        rental = self.rental
        rental.set_returned_video_copies(video_copies)
        for line in rental.rented:
            if line['video_copy'] in video_copies:
                self.assertEquals(line['returned'], True)
            else:
                self.assertEquals(line['returned'], False)

    def test_rental_bonus_points(self):
        """ Test Rental bonus_points method."""
        # bonus should be 5: 2 * 1 new release + 1 * 3 old/regular releases
        self.assertEquals(self.rental.bonus_points(), 5)

    def test_rental_price(self):
        """ Test Rental price method."""
        rental = self.rental
        # c1 new release, 1 day -> 1 * 4 = 4
        # c3 regular release, 5 days ->  3 + 2 * 3 = 9
        # c4 regular release, 2 days -> 3 = 3
        # c5 old release, 7 day -> 3 + 2 * 3 = 9
        # total = 4 + 9 + 3 + 9 = 25
        self.assertEquals(self.rental.price, 25)

        # augment the duration of c1 by 2 days and c3 by 5 days
        # new total should be 25 + 8 + 15 = 48
        rental.rented[0]['duration'] = 3
        rental.rented[1]['duration'] = 10
        self.assertEquals(self.rental.price, 48)
