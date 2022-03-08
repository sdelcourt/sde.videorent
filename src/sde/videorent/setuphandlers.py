# -*- coding: utf-8 -*-

from plone import api
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY

from sde.videorent import _
from sde.videorent.profiles.testing import mock_data

from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.i18n import translate


def isNotCurrentProfile(context):
    return context.readDataFile("sdevideorent_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    remove_default_plone_objects(context)
    create_app_folders(context)


def remove_default_plone_objects(context):
    """
    """
    site = api.portal.get()
    ids_to_delete = [
        'news',
        'events',
        'Members',
        'front-page',
    ]
    to_delete = [getattr(site, oid) for oid in ids_to_delete if hasattr(site, oid)]
    api.content.delete(objects=to_delete)


def create_app_folders(context):
    """
    """
    site = api.portal.get()
    _disable_portlets(site)

    folders_to_create = [
        ['rentals', _('Rentals'), ['Rental']],
        ['films',  _('Films'), ['Film']],
        ['copies',  _('Copies'), ['VideoCopy']],
        ['customers',  _('Customers'), ['Customer']],
    ]

    for folder_id, title, allowed_types in folders_to_create:
        if folder_id not in site.objectIds():
            folder = api.content.create(
                container=site,
                type='Folder',
                id=folder_id,
            )
        else:
            folder = getattr(site, folder_id)

        folder.setTitle(translate(title, context=site.REQUEST))
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(allowed_types)
        folder.setImmediatelyAddableTypes(allowed_types)
        folder.reindexObject(idxs=['Title', 'sortable_title'])
        _disable_portlets(folder)


def _disable_portlets(context):
    for manager_name, src_manager in getUtilitiesFor(IPortletManager, context=context):
        assignment_manager = getMultiAdapter(
            (context, src_manager),
            ILocalPortletAssignmentManager
        )
        assignment_manager.setBlacklistStatus(CONTEXT_CATEGORY, True)
        for category in (GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
            assignment_manager.setBlacklistStatus(
                category,
                assignment_manager.getBlacklistStatus(category)
            )


def create_test_objects(context):
    if context.readDataFile("sdevideorent_test_marker.txt") is None:
        return

    site = api.portal.get()

    customers_folder = site.customers
    for line in mock_data.customers:
        api.content.create(type='Customer', container=customers_folder, **line)

    films_folder = site.films
    for line in mock_data.films:
        api.content.create(type='Film', container=films_folder, **line)

    copies_folder = site.copies
    for line in mock_data.copies:
        film = getattr(films_folder, line['film_id'])
        line['film'] = film.UID()
        api.content.create(type='VideoCopy', container=copies_folder, **line)

    rentals_folder = site.rentals
    for line in mock_data.rentals:
        customer = getattr(customers_folder, line['customer_id'])
        line['customer'] = customer.UID()
        for rent in line['rented']:
            copy = getattr(copies_folder, rent['copy_id'])
            rent['video_copy'] = copy.UID()
        api.content.create(type='Rental', container=rentals_folder, **line)

    api.user.create(**mock_data.test_user)
