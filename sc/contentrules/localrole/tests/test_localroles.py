# -*- coding:utf-8 -*-
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from OFS.interfaces import IObjectManager
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable

from sc.contentrules.localrole.action import LocalRoleAction
from sc.contentrules.localrole.action import LocalRoleEditForm

from plone.app.contentrules.rule import Rule

from sc.contentrules.localrole.tests.base import TestCase

from zope.component.interfaces import IObjectEvent

from Products.PloneTestCase.setup import default_user


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestLocalRoleAction(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
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

    def testExecute(self):
        e = LocalRoleAction()
        e.principal = default_user
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                              IExecutable)
        self.assertEquals(True, ex())
        localroles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles)==localroles)

    def testExecuteWithGroup(self):
        e = LocalRoleAction()
        e.principal = 'Fav Customer'
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                              IExecutable)
        self.assertEquals(True, ex())
        localroles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles)==localroles)

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
        self.failUnless(tuple(e.roles)==localroles)

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
        self.failUnless(tuple(e.roles)==localroles)

    def testExecuteWithError(self):
        e = LocalRoleAction()
        e.principal = '%s-non-existent-user' % default_user
        e.roles = set(['Reader', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(False, ex())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLocalRoleAction))
    return suite
