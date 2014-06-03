# -*- coding:utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.statusmessages.interfaces import IStatusMessage
from sc.contentrules.localrole import MessageFactory as _
from sc.contentrules.localrole.interfaces import ILocalRoleAction
from ZODB.POSException import ConflictError
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface


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
        return _(u"Apply local roles ${roles} to ${principal}",
                 mapping=dict(roles=roles,
                              principal=self.principal))


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
        obj = self.event.object
        mt = getToolByName(self.context, 'portal_membership', None)
        gt = getToolByName(self.context, 'portal_groups', None)
        interpolator = IStringInterpolator(obj)
        if mt is None:
            return False

        roles = list(self.element.roles)
        principal_id = self.element.principal
        #User interpolator to process principal information
        # This way it's possible to set Group_${title}
        # and receive a Group_ContentTitle
        principal_id = interpolator(principal_id).strip()
        principal = mt.getMemberById(principal_id)
        if not principal:
            # Must be a group
            principal = gt.getGroupById(principal_id)

        if not principal:
            self.error(obj, _(u'No user or group found with the provided id.'))
            return False

        actual_roles = list(obj.get_local_roles_for_userid(principal_id))
        wanted_roles = list(set(roles + actual_roles))
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
    """An add form for local roles action.
    """
    form_fields = form.FormFields(ILocalRoleAction)
    label = _(u"Add a Local Role Action")
    description = _(u"An action that applies local roles for a user or group "
                    u"to an object.")

    def create(self, data):
        a = LocalRoleAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class LocalRoleEditForm(EditForm):
    """An edit form for local roles action.
    """
    form_fields = form.FormFields(ILocalRoleAction)
    label = _(u"Edit a Local Role Action")
    description = _(u"An action that applies local roles for a user or group "
                    u"to an object.")
