# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone import api


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if IS_PLONE_5:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
        # Load ZCML
        import sc.contentrules.localrole
        self.loadZCML(package=sc.contentrules.localrole)

    def setUpPloneSite(self, portal):
        if IS_PLONE_5:
            self.applyProfile(portal, 'plone.app.contenttypes:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.contentrules.localrole:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.contentrules.localrole:Functional',
)
