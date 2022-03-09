# -*- coding: utf-8 -*-

from plone.indexer import indexer

from sde.videorent.content.rental import IRental


@indexer(IRental)
def rented_video_copies(rental):
    rented_videos = [line['video_copy'] for line in rental.rented if not line['returned']]
    return rented_videos
