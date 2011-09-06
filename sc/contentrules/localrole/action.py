# -*- coding:utf-8 -*-
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema

from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError

from plone.app.contentrules.browser.formhelper import AddForm, EditForm

from sc.contentrules.localrole.interfaces import ILocalRoleAction

from sc.contentrules.localrole import MessageFactory as _


class LocalRoleAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(ILocalRoleAction, IRuleElementData)

    principal = ''
    roles = ''
    element = "sc.contentrules.localrole.ApplyLocalRole"

    @property
    def summary(self):
        roles = ', '.join(self.roles)
        return _(u"Apply localrole ${roles} to ${principal}",
                 mapping=dict(role=[roles],principal=self.principal))


class LocalRoleActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, ILocalRoleAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        mt = getToolByName(self.context, 'portal_membership', None)
        gt = getToolByName(self.context, 'portal_groups', None)
        if mt is None:
            return False

        obj = self.event.object
        roles = list(self.element.roles)
        principal_id = self.element.principal
        principal = mt.getMemberById(principal_id)
        if not principal:
            # Must be a group
            principal = gt.getGroupById(principal_id)

        if not principal:
            self.error(obj, _(u'No user or group found with the provided id.'))

        existing_roles = list(obj.get_local_roles_for_userid(userid=principal_id))
        wanted_roles = list(set(roles + existing_roles))

        try:
            obj.manage_setLocalRoles(principal_id, list(wanted_roles))
        except ConflictError, e:
            raise e
        except Exception, e:
            self.error(obj, str(e))
            return False

        return True

    def error(self, obj, error):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(u"Unable to apply local roles on ${name}: ${error}",
                          mapping={'name': title, 'error': error})
            IStatusMessage(request).addStatusMessage(message, type="error")


class LocalRoleAddForm(AddForm):
    """An add form for localrole action.
    """
    form_fields = form.FormFields(ILocalRoleAction)
    label = _(u"Add a Local Role Action")
    description = _(u"An action that applies a local role for a user or group \
                      on an object.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = LocalRoleAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class LocalRoleEditForm(EditForm):
    """An edit form for workflow rule actions.
    """
    form_fields = form.FormFields(ILocalRoleAction)
    label = _(u"Edit a Local Role Action")
    description = _(u"An action that applies a local role for a user or group \
                      on an object.")
    form_name = _(u"Configure element")
