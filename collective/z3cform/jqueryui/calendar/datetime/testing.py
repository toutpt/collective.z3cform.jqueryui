from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class PFWDTLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.formwidget.datetime
        self.loadZCML(package=plone.formwidget.datetime)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.formwidget.datetime:default')


PFWDT_FIXTURE = PFWDTLayer()
PFWDT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PFWDT_FIXTURE,),
    name="PFWDT:Integration")
