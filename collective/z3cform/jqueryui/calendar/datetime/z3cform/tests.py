from StringIO import StringIO
from Testing import ZopeTestCase as ztc
from z3c.form.interfaces import IFieldWidget
from z3c.form.testing import TestRequest
from zope.app.testing import setup
from zope.configuration import xmlconfig

import doctest
import plone.formwidget.datetime.z3cform
import unittest
import z3c.form
import zope.app.component
import zope.component
import zope.schema


class WidgetTestCase(object):

    def setUp(self):
        self.root = setup.placefulSetUp(True)
        xmlconfig.XMLConfig('meta.zcml', zope.component)()
        xmlconfig.XMLConfig('meta.zcml', zope.app.component)()
        try:
            xmlconfig.XMLConfig('configure.zcml', zope.i18n)()
        except IOError:
            # Zope 2.10
            xmlconfig.xmlconfig(StringIO('''
            <configure xmlns="http://namespaces.zope.org/zope">
               <utility
                  provides="zope.i18n.interfaces.INegotiator"
                  component="zope.i18n.negotiator.negotiator" />

               <include package="zope.i18n.locales" />
            </configure>
             '''))
        xmlconfig.XMLConfig('meta.zcml', zope.i18n)()
        xmlconfig.XMLConfig('meta.zcml', z3c.form)()
        xmlconfig.XMLConfig('configure.zcml', plone.formwidget.datetime.z3cform)()

    def tearDown(self):
        setup.placefulTearDown()

    def testrequest(self, lang="en", form={}):
        return TestRequest(HTTP_ACCEPT_LANGUAGE=lang, form=form)

    def setupWidget(self, field, lang="en"):
        request = self.testrequest(lang=lang)
        widget = zope.component.getMultiAdapter((field, request),
                                                IFieldWidget)
        widget.id = 'foo'
        widget.name = 'bar'
        return widget


def test_suite():
    return unittest.TestSuite((
        ztc.ZopeDocFileSuite(
            'widget_date.txt',
            'widget_datetime.txt',
            'widget_monthyear.txt',
            'converter.txt',
            'issues.txt',
            test_class=WidgetTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE |
                        doctest.ELLIPSIS |
                        doctest.REPORT_UDIFF,
            ),
        ))
