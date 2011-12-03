import mock
import unittest2 as unittest


class TestBaseWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.at.browser.widget import Base
        context = mock.Mock()
        request = mock.Mock()
        return Base(context, request)

    def test_subclass(self):
        from plone.formwidget.datetime.at.browser.widget import Base
        from Products.Five import BrowserView
        self.assertTrue(issubclass(Base, BrowserView))

    def test_macros(self):
        instance = self.createInstance()
        instance.template = mock.Mock()
        instance.template.macros = 'macros'
        self.assertEqual(instance.macros, 'macros')
