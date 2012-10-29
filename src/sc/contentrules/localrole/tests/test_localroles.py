# -*- coding:utf-8 -*-

import unittest2 as unittest

from OFS.interfaces import IObjectManager

from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable

from sc.contentrules.localrole.action import LocalRoleAction
from sc.contentrules.localrole.action import LocalRoleEditForm
from sc.contentrules.localrole.testing import INTEGRATION_TESTING


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestLocalRoleAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        #setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        # setup default user
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
        gt = self.portal.portal_groups
        gt.addGroup('Fav Customer', title='Our Fav Customer', roles=())

    def testRegistered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.localrole.ApplyLocalRole')
        self.assertEquals('sc.contentrules.localrole.ApplyLocalRole',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(IObjectManager, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.localrole.ApplyLocalRole')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        acl_users = getToolByName(self.portal, 'acl_users')
        default_user = acl_users.getUserById('user1')

        addview.createAndAdd(data={'principal': default_user,
                                   'roles': set(['Reader', ])})

        e = rule.actions[0]
        self.failUnless(isinstance(e, LocalRoleAction))
        self.assertEquals(default_user, e.principal)
        self.assertEquals(set(['Reader', ]), e.roles)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.localrole.ApplyLocalRole')
        e = LocalRoleAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, LocalRoleEditForm))

    def testActionSummary(self):
        e = LocalRoleAction()
        e.principal = '${title}'
        e.roles = set(['Reader', ])
        summary = u"Apply local roles ${roles} to ${principal}"
        self.assertEquals(summary, e.summary)

    def testExecute(self):
        e = LocalRoleAction()
        e.principal = 'user1'
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        localroles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles) == localroles)

    def testExecuteWithGroup(self):
        e = LocalRoleAction()
        e.principal = 'Fav Customer'
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        localroles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles) == localroles)

    def testExecuteInterp(self):
        # Setup scenario
        self.portal.portal_registration.addMember('mrfoo', '12345', ())
        self.portal.invokeFactory('Folder', 'mrfoo', title='mrfoo')
        folder = self.portal['mrfoo']
        e = LocalRoleAction()
        e.principal = '${title}'
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        localroles = folder.get_local_roles_for_userid(userid='mrfoo')
        self.failUnless(tuple(e.roles) == localroles)

    def testExecuteInterpGroup(self):
        # Setup scenario
        self.portal.invokeFactory('Folder', 'customer', title='Fav Customer')
        folder = self.portal['customer']
        e = LocalRoleAction()
        e.principal = '${title}'
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        localroles = folder.get_local_roles_for_userid(userid='Fav Customer')
        self.failUnless(tuple(e.roles) == localroles)

    def testExecuteWithError(self):
        acl_users = getToolByName(self.portal, 'acl_users')
        e = LocalRoleAction()
        e.principal = '%s-non-existent-user' % acl_users.getUserById('user1')
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(False, ex())

    def testExecuteAsMember(self):
        e = LocalRoleAction()
        e.principal = 'user1'
        e.roles = set(['Reader', ])
        # User will have only Member role in the
        # context
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        localroles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles) == localroles)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
