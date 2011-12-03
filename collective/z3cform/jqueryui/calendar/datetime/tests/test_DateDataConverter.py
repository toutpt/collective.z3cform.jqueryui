import mock
import unittest2 as unittest


class TestDateDataConverter(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.converter import DateDataConverter
        field = mock.Mock()
        widget = mock.Mock()
        return DateDataConverter(field, widget)

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.converter import DateDataConverter
        from z3c.form.converter import BaseDataConverter
        self.assertTrue(DateDataConverter, BaseDataConverter)

    def test_instance(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.converter import DateDataConverter
        self.assertTrue(isinstance(instance, DateDataConverter))

    def test_toWidgetValue__value_is_missing(self):
        instance = self.createInstance()
        value = instance.field.missing_value
        self.assertEqual(
            instance.toWidgetValue(value),
            ('', '', '')
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

    def test_toFieldValue_no_value(self):
        instance = self.createInstance()
        value = [None]
        instance.field.missing_value = 'missing_value'
        self.assertEqual(
            instance.toFieldValue(value),
            'missing_value'
        )

    def test_toFieldValue_map_ValueError(self):
        instance = self.createInstance()
        value = 'abcde'
        from plone.formwidget.datetime.z3cform.interfaces import DateValidationError
        self.assertRaises(
            DateValidationError,
            lambda: instance.toFieldValue(value)
        )

    def test_toFieldValue_date_ValueError(self):
        instance = self.createInstance()
        value = '012'
        from plone.formwidget.datetime.z3cform.interfaces import DateValidationError
        self.assertRaises(
            DateValidationError,
            lambda: instance.toFieldValue(value)
        )

    @mock.patch('plone.formwidget.datetime.z3cform.converter.date')
    def test_toFieldValue_no_ValueError(self, date):
        instance = self.createInstance()
        value = '123'
        date.return_value = 'date'
        self.assertEqual(
            instance.toFieldValue(value),
            'date'
        )
