import mock
import unittest2 as unittest


class TestDatetimeDataConverter(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.converter import DatetimeDataConverter
        field = mock.Mock()
        widget = mock.Mock()
        return DatetimeDataConverter(field, widget)

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.converter import DatetimeDataConverter
        from plone.formwidget.datetime.z3cform.converter import DateDataConverter
        self.assertTrue(DatetimeDataConverter, DateDataConverter)

    def test_instance(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.converter import DatetimeDataConverter
        self.assertTrue(isinstance(instance, DatetimeDataConverter))

    def test_toWidgetValue__value_is_missing(self):
        instance = self.createInstance()
        value = instance.field.missing_value
        self.assertEqual(
            instance.toWidgetValue(value),
            ('', '', '', '00', '00')
        )

    def test_toWidgetValue__value_is_not_missing(self):
        instance = self.createInstance()
        value = mock.Mock()
        value.year = 'year'
        value.month = 'month'
        value.day = 'day'
        value.hour = 'hour'
        value.minute = 'minute'
        self.assertEqual(
            instance.toWidgetValue(value),
            ('year', 'month', 'day', 'hour', 'minute')
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
        from plone.formwidget.datetime.z3cform.interfaces import DatetimeValidationError
        self.assertRaises(
            DatetimeValidationError,
            lambda: instance.toFieldValue(value)
        )

    def test_toFieldValue_date_ValueError(self):
        instance = self.createInstance()
        value = '012'
        from plone.formwidget.datetime.z3cform.interfaces import DatetimeValidationError
        self.assertRaises(
            DatetimeValidationError,
            lambda: instance.toFieldValue(value)
        )

    @mock.patch('plone.formwidget.datetime.z3cform.converter.datetime')
    def test_toFieldValue_no_ValueError(self, datetime):
        instance = self.createInstance()
        value = '123'
        datetime.return_value = 'datetime'
        self.assertEqual(
            instance.toFieldValue(value),
            'datetime'
        )
