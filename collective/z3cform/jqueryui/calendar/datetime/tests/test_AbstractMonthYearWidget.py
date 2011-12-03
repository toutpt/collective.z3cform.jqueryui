import unittest2 as unittest


class TestAbstractMonthYearWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.base import AbstractMonthYearWidget
        return AbstractMonthYearWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.base import AbstractMonthYearWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        self.assertTrue(issubclass(AbstractMonthYearWidget, AbstractDateWidget))

    def test_instance__klass(self):
        instance = self.createInstance()
        self.assertEqual(instance.klass, u'monthyear-widget')

    def test_instance__empty_value(self):
        instance = self.createInstance()
        self.assertEqual(instance.empty_value, ('', '', 1))

    def test_instance__value(self):
        instance = self.createInstance()
        self.assertEqual(instance.value, ('', '', 1))
