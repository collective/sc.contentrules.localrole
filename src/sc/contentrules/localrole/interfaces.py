# -*- coding: utf-8 -*-
from sc.contentrules.localrole import MessageFactory as _
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Set
from zope.schema import TextLine


class ILocalRoleAction(Interface):
    """An action used to apply a local role to an object
    """

    principal = TextLine(title=_(u"Username / Group name"),
                         description=_(u"Please inform the username or "
                                       u"groupname that will be used by "
                                       u"this action.  Use  ${title} in "
                                       u"this field to use the content "
                                       u"title as the value for this field."),
                         required=True)

    roles = Set(title=_(u"Roles"),
                description=_(u"Roles to be assigned to user/group "
                              u"in the object."),
                required=True,
                value_type=Choice(vocabulary='plone.app.vocabularies.Roles')
                )
