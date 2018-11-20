# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)
        # Load ZCML
        import sc.contentrules.localrole
        self.loadZCML(package=sc.contentrules.localrole)
        if not IS_PLONE_5:
            # The tests will fail with a
            # `ValueError: Index of type DateRecurringIndex not found` unless
            # the product 'Products.DateRecurringIndex' is installed.
            z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
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
