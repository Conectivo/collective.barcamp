# -*- coding: utf-8 -*-

from collective.barcamp.interfaces.barcampevent import IBarcampEvent
from plone.indexer.decorator import indexer


@indexer(IBarcampEvent)
def barcampevent_start(obj, **kw):
    return obj.startDate


@indexer(IBarcampEvent)
def barcampevent_end(obj, **kw):
    return obj.endDate
