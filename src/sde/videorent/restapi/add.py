# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service

from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class RentalPost(Service):
    """
    Rental POST endpoint.
    @params:
    {
        "customer": "customer_UID",
        "rented": [
            "video_copy": "video_copy_1_UID", "duration": days,
            ...,
            "video_copy": "video_copy_1_UID", "duration": days
        ]
    }
    @return: Rental object created
    customer bonus points have also been updated accordingly
    """

    def __init__(self, context, request):
        super(Service, self).__init__(context, request)
        self.params = []

    def reply(self):
        params = json.loads(self.request.get("BODY", "{}"))
        for line in params['rented']:
            line['returned'] = False
        new_id = 'rental-{}'.format(len(self.context.objectValues()))
        new_rental = api.content.create(
            type='Rental',
            id=new_id,
            container=self.context,
            **params
        )
        serializer = queryMultiAdapter((new_rental, self.request), ISerializeToJson)
        return serializer()
