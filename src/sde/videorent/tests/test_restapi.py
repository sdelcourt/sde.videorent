# -*- coding: utf-8 -*-

from datetime import timedelta

from plone.app.testing import login
from plone.restapi.testing import RelativeSession

from sde.videorent.testing import FunctionalTestCase

import transaction


class TestRestApi(FunctionalTestCase):
    """Base class for defining videorent restapi test cases."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.portal_url = self.portal.absolute_url()
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = ('manager', 'manager')
        login(self.portal, 'manager')
        self.copies = self.portal.copies
        self.customers = self.portal.customers
        self.rentals_folder_url = self.portal.rentals.absolute_url()
        self.rentals = self.portal.rentals
        self.rental = self.portal.rentals.rental

    def tearDown(self):
        self.api_session.close()
        transaction.abort()

    def test_add_rental_service(self):
        """ Test the POST endpoint @rental."""

        customer = self.customers.gerard
        customer_previous_bonus_points = customer.bonus_points

        rental_params = {
            "customer": customer.UID(),
            "rented": [
                {"video_copy": self.copies.c1.UID(), "duration": 5},
                {"video_copy": self.copies.c5.UID(), "duration": 5}
            ]
        }
        endpoint_url = "{0}/@rental".format(self.rentals_folder_url)
        response = self.api_session.post(endpoint_url, json=rental_params)

        transaction.begin()
        self.assertEqual(response.status_code, 200, response.content)
        response = response.json()

        # check if the Rental object has been created
        self.assertTrue(response["id"] in self.rentals.objectIds())
        # check the attributes of the Rental returned
        self.assertEquals(
            response["customer"]["title"].encode('utf-8'),
            self.customers.gerard.Title()
        )
        self.assertEquals(
            response["rented"],
            [
                {"video_copy": self.copies.c1.UID(), "duration": 5, "returned": False},
                {"video_copy": self.copies.c5.UID(), "duration": 5, "returned": False},
            ]
        )
        # bonus points of this rental should be 3 (one new release, one old)
        self.assertEquals(response["bonus_points"], 3)

        # customer point should have been updated
        self.assertEqual(
            customer.bonus_points,
            customer_previous_bonus_points + response["bonus_points"]
        )

    def test_update_rented_without_lateness(self):
        """ Test the patch endpoint @rented."""

        # return VideoCopies c1 and c3
        video_copies = [self.copies.c1.UID(), self.copies.c3.UID()]
        endpoint_url = "{0}/@rented".format(self.rentals_folder_url)
        json = video_copies
        response = self.api_session.patch(endpoint_url, json=json)

        transaction.begin()
        self.assertEqual(response.status_code, 200, response.content)
        response = response.json()

        # VideoCopies c1 and c3 status  should be 'returned'
        for line in response['rentals'][0]['rented']:
            if line['video_copy'] in video_copies:
                self.assertEquals(line['returned'], True)
            else:
                self.assertEquals(line['returned'], False)

        # no late fees as we returned the copies the same day of the rental
        self.assertEqual(response['rentals'][0]['late_fees'], [])

    def test_update_rented_with_lateness(self):
        """ Test the patch endpoint @rented with late returns."""

        rental = self.rental
        # set -4 days to the start date so the VideoCopy c1 is late
        rental.start_date = rental.start_date - timedelta(days=4)
        transaction.commit()

        # return VideoCopies c1 and c3
        video_copies = [self.copies.c1.UID(), self.copies.c3.UID()]
        endpoint_url = "{0}/@rented".format(self.rentals_folder_url)
        json = video_copies
        response = self.api_session.patch(endpoint_url, json=json)

        transaction.begin()
        self.assertEqual(response.status_code, 200, response.content)
        response = response.json()

        # VideoCopies c1 and c3 status should be 'returned'
        for line in response['rentals'][0]['rented']:
            if line['video_copy'] in video_copies:
                self.assertEquals(line['returned'], True)
            else:
                self.assertEquals(line['returned'], False)

        late_fees = response['late_fees']
        # we should have one late fee
        self.assertEquals(len(late_fees), 1)
        c1_late_fee = late_fees[0]
        # late fee is for c1
        self.assertEquals(c1_late_fee['video_copy'], self.copies.c1.UID())
        # VideoCopy c1 was late by 3 days
        self.assertEquals(c1_late_fee['late_days'], 3)
        # and has 12 euros fee (3 days * premium price 4 euros)
        self.assertEquals(c1_late_fee['fee'], 12)
