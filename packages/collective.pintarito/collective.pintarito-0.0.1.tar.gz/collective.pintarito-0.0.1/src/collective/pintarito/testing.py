from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.pintarito


class CollectivePintaritoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.pintarito)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.pintarito:default")


COLLECTIVE_PINTARITO_FIXTURE = CollectivePintaritoLayer()


COLLECTIVE_PINTARITO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PINTARITO_FIXTURE,),
    name="CollectivePintaritoLayer:IntegrationTesting",
)


COLLECTIVE_PINTARITO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PINTARITO_FIXTURE,),
    name="CollectivePintaritoLayer:FunctionalTesting",
)
