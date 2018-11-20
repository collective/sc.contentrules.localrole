# -*- coding: utf-8 -*-
from sc.contentrules.localrole import MessageFactory as _
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema import Choice
from zope.schema import Set
from zope.schema import TextLine


class ILocalRoleAction(Interface):
    """An action used to apply a local role to an object
    """

    principal = TextLine(title=_(u"User/Group ID"),
                         description=_(u"Enter the user or group id who "
                                       u"should receive the permission "
                                       u"in sharing (or pick a field below)"),
                         required=False)

    field = Choice(title=_(u"Field with User/Group ID"),
                   description=_(u"Pick a field which contains user/group "
                                 u"ID to receive the permission. If the "
                                 u"field is not found not permission will "
                                 u"be set in sharing."),
                   required=False,
                   vocabulary=u'sc.contentrules.localrole.allfields',
                   )

    roles = Set(title=_(u"Roles"),
                description=_(u"Roles to be assigned to user/group "
                              u"in the object."),
                required=True,
                value_type=Choice(vocabulary='plone.app.vocabularies.Roles')
                )

    @invariant
    def id_invariant(data):
        error_message = _(u'You should fill one of "User/Group ID" or '
                          u'"Field with User/Group ID", but not both.')
        if data.principal is None and data.field is None:
            raise Invalid(error_message)
        if data.principal is not None and data.field is not None:
            raise Invalid(error_message)
