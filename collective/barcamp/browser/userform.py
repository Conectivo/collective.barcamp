# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from collective.barcamp import barcampMessageFactory as _
from collective.barcamp.unrestrictor import unrestrictedExec
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.z3cform.layout import wrap_form

from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import interface
from zope import schema
from zope.component import queryUtility
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

LEVEL_VOCAB = SimpleVocabulary([
    SimpleTerm(value=u'beginner', title=_(u'Beginner')),
    SimpleTerm(value=u'intermediate', title=_(u'Intermediate')),
    SimpleTerm(value=u'advanced', title=_(u'Advanced'))
])

STYPE_VOCAB = SimpleVocabulary([
    SimpleTerm(value=u'talk', title=_(u'Talk')),
    SimpleTerm(value=u'hackfest', title=_(u'Hackfest')),
    SimpleTerm(value=u'workshop', title=_(u'Workshop')),
    SimpleTerm(value=u'discussion', title=_(u'Discussion'))
])


class ISessionSubmissionForm(interface.Interface):
    title = schema.TextLine(title=_(u'Title'))
    description = schema.Text(title=_(u'Description'), required=True)
    speaker = schema.TextLine(title=_(u'Speaker'), required=True)
    subject = schema.Text(
        title=_(u'Tags'),
        description=_(u'Enter one tag per line, multiple words allowed.'),
        required=False
    )
    level = schema.Choice(
        title=_(u'Level'),
        vocabulary=LEVEL_VOCAB
    )
    session_type = schema.Choice(
        title=_(u'Session Type'),
        vocabulary=STYPE_VOCAB
    )


class SessionSubmissionForm(form.Form):
    fields = field.Fields(ISessionSubmissionForm)
    ignoreContext = True  # don't use context to get widget data
    label = _(u'Register a session')

    @button.buttonAndHandler(_(u'Submit'))
    def handleApply(self, action):
        data, errors = self.extractData()
        typestool = getToolByName(self.context, 'portal_types')
        wftool = getToolByName(self.context, 'portal_workflow')
        identifier = queryUtility(IIDNormalizer).normalize(data['title'])
        # if not self.context.has_key('sessions'):
        if 'sessions' not in self.context:
            unrestrictedExec(
                typestool.constructContent,
                type_name='Folder',
                container=self.context,
                id='sessions'
            )
            unrestrictedExec(
                self.context['sessions'].setTitle,
                'Sessions'
            )
            unrestrictedExec(
                wftool.doActionFor,
                self.context['sessions'],
                'publish'
            )
            self.context['sessions'].reindexObject()
        container = self.context['sessions']
        identifier = str(len(container.keys()) + 1)
        if data['subject']:
            subject = list([i for i in data['subject'].split('\n') if i])
        else:
            subject = []
        del data['subject']

        level = data['level']
        del data['level']
        speaker = data['speaker']
        del data['speaker']
        session_type = data['session_type']
        del data['session_type']

        unrestrictedExec(
            typestool.constructContent,
            type_name='BarcampSession',
            container=container,
            id=identifier,
            **data
        )

        content = container[identifier]
        schema = content.Schema()
        schema['subject'].set(content, subject)
        schema['level'].set(content, level)
        schema['speaker'].set(content, speaker)
        schema['session_type'].set(content, session_type)
        schema['startDate'].set(content, self.context.startDate)
        schema['endDate'].set(content, self.context.endDate)
        unrestrictedExec(
            wftool.doActionFor,
            container[identifier],
            'publish'
        )
        content.reindexObject()
        self.request.response.redirect(content.absolute_url())

SessionSubmissionView = wrap_form(SessionSubmissionForm)


class IRegistrationForm(interface.Interface):
    title = schema.TextLine(title=_(u'Full name'))
    email = schema.TextLine(
        title=_(u'Email address'),
        description=_(u'We will not publish this. We collect this to send confirmed details and a reminder just before the camp.')
    )
    description = schema.Text(
        title=_(u'Short Bio'),
        description=_(u'Where you\'re from, where you work / study, brief self-description'),
        required=True
    )
    online_presence = schema.TextLine(
        title=_(u'Online presence'),
        description=_(u'URL to blog / website / Google+ / Twitter / Facebook / etc'),
        required=False
    )


class RegistrationForm(form.Form):
    fields = field.Fields(IRegistrationForm)
    ignoreContext = True  # don't use context to get widget data
    label = _(u'Register')

    @button.buttonAndHandler(_(u'Register'))
    def handleApply(self, action):
        data, errors = self.extractData()
        typestool = getToolByName(self.context, 'portal_types')
        # wftool = getToolByName(self.context, 'portal_workflow')
        plone_utils = getToolByName(self.context, 'plone_utils')
        # if not self.context.has_key('registrations'):
        if 'registrations' not in self.context:
            unrestrictedExec(
                typestool.constructContent,
                type_name='Folder',
                container=self.context,
                id='registrations'
            )
            unrestrictedExec(
                self.context['registrations'].setTitle,
                'Registrations'
            )
            cschema = self.context['registrations'].Schema()
            cschema['excludeFromNav'].set(
                self.context['registrations'],
                True
            )
            self.context['registrations'].reindexObject()
        container = self.context['registrations']
        identifier = str(len(container.keys()) + 1)

        unrestrictedExec(
            typestool.constructContent,
            type_name='BarcampParticipant',
            container=container,
            id=identifier,
            **data
        )
        plone_utils.addPortalMessage(
            _(u'Thank you for your submission. You are now registered'),
            'info'
        )
        self.request.response.redirect(self.context.absolute_url())

RegistrationView = wrap_form(RegistrationForm)
