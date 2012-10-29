# -*- coding: utf-8 -*-
import re
from zope.interface import implements
from zope.interface import Interface
from zope import schema

from sc.contentrules.localrole import MessageFactory as _


class ILocalRoleAction(Interface):
    """An action used to apply a local role to an object
    """

    principal = schema.TextLine(title=_(u"Username / Group name"),
                      description=_(u"Please inform the username or groupname \
                                      that will be used by this action."),
                      required=True,
                )

    roles = schema.Set(title=_(u"Roles"),
                         description=_(u"Roles to be assigned to user/group \
                                         in the object."),
                         required=True,
                         value_type=schema.Choice(
                                    vocabulary='plone.app.vocabularies.Roles',
                ))
