# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service

from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class RentedPatch(Service):
    """
    Update the rented attribute of all the rentals having
    the returned VideoCopies still to be returned.
    """

    def __init__(self, context, request):
        super(Service, self).__init__(context, request)
        self.params = []

    def reply(self):
        copies_to_return = json.loads(self.request.get("BODY", "[]"))
        catalog = api.portal.get_tool('portal_catalog')
        rental_brains = catalog(rented_video_copies=copies_to_return)

        # get the late fees and update the rentals
        result = {'rentals': [], 'late_fees': []}
        for rental_brain in rental_brains:
            rental = rental_brain.getObject()
            # first get the late fees
            late_fees = rental.get_video_copies_late_fees(copies_to_return)
            result['late_fees'].extend(late_fees)
            # then update the rental
            rental.set_returned_video_copies(copies_to_return)
            rental.reindexObject()
            serializer = queryMultiAdapter((rental, self.request), ISerializeToJson)
            result['rentals'].append(serializer())

        return result
