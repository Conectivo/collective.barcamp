"""Definition of the BarcampSession content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.content.event import ATEventSchema, ATEvent

# -*- Message Factory Imported Here -*-

from collective.barcamp.interfaces import IBarcampSession
from collective.barcamp.config import PROJECTNAME
from collective.barcamp import barcampMessageFactory as _
from DateTime import DateTime


BarcampSessionSchema = ATEventSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'speaker',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Speaker"),
        ),
    ),
    atapi.StringField(
        'level',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u"Level"),
        ),
        vocabulary=[_(u"Beginner"),_(u"Intermediate"), _(u"Advanced")]
    ),
    atapi.StringField(
        'session_type',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u"Session Type"),
        ),
        vocabulary=[_(u"Talk"), _(u"Discussion"), _(u"Workshop"), _(u"Meta")]
    ),

))

BarcampSessionSchema['startDate'].widget.label=_(u"Session Starts")
BarcampSessionSchema['endDate'].widget.label=_(u"Session Ends")

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BarcampSessionSchema, moveDiscussion=False)
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou


class BarcampSession(ATEvent):
    """A Barcamp Session"""
    implements(IBarcampSession, ILoveThumbsDontYou)

    meta_type = "BarcampSession"
    schema = BarcampSessionSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    speaker = atapi.ATFieldProperty('speaker')
    level = atapi.ATFieldProperty('level')
    session_type = atapi.ATFieldProperty('session_type')


atapi.registerType(BarcampSession, PROJECTNAME)
