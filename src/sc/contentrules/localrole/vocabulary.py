# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def get_fields(portal_type):
    """List all fields from portal_type and behaviors
    https://stackoverflow.com/q/12178669/2116850
    """
    fti = getUtility(IDexterityFTI, name=portal_type)
    schema = fti.lookupSchema()
    fields = schema.names()
    for bname in fti.behaviors:
        factory = getUtility(IBehavior, bname)
        behavior = factory.interface
        fields += behavior.names()
    return fields


def AllFieldsVocabulary(context):
    """Vocabulary factory for fields in content types."""
    factory = getUtility(
        IVocabularyFactory, 'plone.app.vocabularies.ReallyUserFriendlyTypes')
    vocabulary = factory(None)
    fields = []
    for term in vocabulary:
        portal_type = term.value
        try:
            fields += get_fields(portal_type)
        except ComponentLookupError:
            pass
    return SimpleVocabulary([
        SimpleTerm(value=field) for field in set(fields)
    ])

