# -*- coding:utf-8 -*-
from zope.interface import implements, Interface
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

from DateTime import DateTime

class DummyEvent(object):
    implements(IObjectEvent)
    
    def __init__(self, object):
        self.object = object

class TestLocalRoleAction(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']

    def testRegistered(self): 
        element = getUtility(IRuleAction, name='sc.contentrules.localrole.ApplyLocalRole')
        self.assertEquals('sc.contentrules.localrole.ApplyLocalRole', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(IObjectManager, element.for_)
        self.assertEquals(IObjectEvent, element.event)
    
    def testInvokeAddView(self): 
        element = getUtility(IRuleAction, name='sc.contentrules.localrole.ApplyLocalRole')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')
        
        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        
        addview.createAndAdd(data={'principal' : default_user,
                                    'roles':set(['Reader',])})
        
        e = rule.actions[0]
        self.failUnless(isinstance(e, LocalRoleAction))
        self.assertEquals(default_user, e.principal)
        self.assertEquals(set(['Reader',]), e.roles)
    
    def testInvokeEditView(self): 
        element = getUtility(IRuleAction, name='sc.contentrules.localrole.ApplyLocalRole')
        e = LocalRoleAction()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview, LocalRoleEditForm))

    def testExecute(self): 
        e = LocalRoleAction()
        e.principal = default_user
        e.roles = set(['Reader',])
        
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)), IExecutable)
        self.assertEquals(True, ex())
        local_roles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failUnless(tuple(e.roles)==local_roles)        

    def testExecuteWithError(self): 
        #TODO
        e = LocalRoleAction()
        e.principal = '%s-non-existent-user' % default_user
        e.roles = set(['Reader',])
        
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)), IExecutable)
        self.assertEquals(True, ex())
        local_roles = self.folder.get_local_roles_for_userid(userid=e.principal)
        self.failIf(tuple(e.roles)==local_roles)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLocalRoleAction))
    return suite
