import mock
import unittest2 as unittest


class TestMonthYearDataConverter(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.converter import MonthYearDataConverter
        field = mock.Mock()
        widget = mock.Mock()
        return MonthYearDataConverter(field, widget)

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.converter import MonthYearDataConverter
        from plone.formwidget.datetime.z3cform.converter import DateDataConverter
        self.assertTrue(MonthYearDataConverter, DateDataConverter)

    def test_instance(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.converter import MonthYearDataConverter
        self.assertTrue(isinstance(instance, MonthYearDataConverter))

    def test_toWidgetValue__value_is_missing(self):
        instance = self.createInstance()
        value = instance.field.missing_value
        self.assertEqual(
            instance.toWidgetValue(value),
            ('', '', '1')
        )

    def test_toWidgetValue__value_is_not_missing(self):
        instance = self.createInstance()
        value = mock.Mock()
        value.year = 'year'
        value.month = 'month'
        value.day = 'day'
        self.assertEqual(
            instance.toWidgetValue(value),
            ('year', 'month', 'day')
        )
