import mock
import unittest2 as unittest


class TestAbstractDatetimeWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        return AbstractDatetimeWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        self.assertTrue(issubclass(AbstractDatetimeWidget, AbstractDateWidget))

    def test_instance__klass(self):
        instance = self.createInstance()
        self.assertEqual(instance.klass, u'datetime-widget')

    def test_instance__empty_value(self):
        instance = self.createInstance()
        self.assertEqual(instance.empty_value, ('', '', '', '00', '00'))

    def test_instance__value(self):
        instance = self.createInstance()
        self.assertEqual(instance.value, ('', '', '', '00', '00'))

    def test_instance__ampm(self):
        instance = self.createInstance()
        self.assertFalse(instance.ampm)

    def test__dtformatter(self):
        instance = self.createInstance()
        getFormatter = mock.Mock()
        instance.request = mock.Mock()
        instance.request.locale.dates.getFormatter = getFormatter
        instance._dtformatter
        getFormatter.assert_called_with('dateTime', 'short')

    @mock.patch('plone.formwidget.datetime.base.datetime')
    def test__dtvalue(self, datetime):
        instance = self.createInstance()
        value = '123'
        instance._dtvalue(value)
        datetime.assert_called_with(1, 2, 3)

    def test_hour_is_not_None(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = '11'
        self.assertEqual(instance.hour, '11')

    def test_hour_is_None_value_not_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '1234'
        instance.empty_value = '4567'
        self.assertEqual(instance.hour, '4')

    def test_hour_is_None_value_is_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '1234'
        instance.empty_value = '1354'
        self.assertFalse(instance.hour)

    def test_minute_is_not_None(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = '55'
        self.assertEqual(instance.minute, '55')

    def test_minute_is_None_value_not_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '12345'
        instance.empty_value = '45678'
        self.assertEqual(instance.minute, '8')

    def test_minute_is_None_value_is_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '12345'
        instance.empty_value = '13465'
        self.assertFalse(instance.minute)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_is_pm__True(self, hour):
        instance = self.createInstance()
        instance.hour = 12
        self.assertTrue(instance.is_pm())

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_is_pm__False(self, hour):
        instance = self.createInstance()
        instance.hour = 11
        self.assertFalse(instance.is_pm())

    def test_minutes(self):
        instance = self.createInstance()
        instance.padded_minute = mock.Mock(return_value='minute')
        self.assertEqual(len(instance.minutes), 60)
        self.assertEqual(
            instance.minutes[0],
            {'value': 0, 'name': 'minute'}
        )
        self.assertEqual(
            instance.minutes[-1],
            {'value': 59, 'name': 'minute'}
        )

    def test_hours(self):
        instance = self.createInstance()
        instance.padded_hour = mock.Mock(return_value='hour')
        self.assertEqual(len(instance.hours), 24)
        self.assertEqual(
            instance.hours[0],
            {'value': 0, 'name': 'hour'}
        )
        self.assertEqual(
            instance.hours[-1],
            {'value': 23, 'name': 'hour'}
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_padded_hour_None(self, hour):
        instance = self.createInstance()
        instance.hour = None
        self.assertFalse(instance.padded_hour())

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_padded_hour_ampm(self, hour):
        instance = self.createInstance()
        instance.ampm = True
        instance.is_pm = mock.Mock()
        instance.hour = 14
        instance._padded_value = mock.Mock()
        instance.padded_hour()
        instance._padded_value.assert_called_with('2')

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_padded_hour_ampm_False(self, hour):
        instance = self.createInstance()
        instance.ampm = False
        instance.is_pm = mock.Mock()
        instance.hour = 14
        instance._padded_value = mock.Mock()
        instance.padded_hour()
        instance._padded_value.assert_called_with(14)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_padded_hour_is_pm_False(self, hour):
        instance = self.createInstance()
        instance.ampm = True
        instance.is_pm = mock.Mock(return_value=False)
        instance.hour = 14
        instance._padded_value = mock.Mock()
        instance.padded_hour()
        instance._padded_value.assert_called_with(14)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    def test_padded_hour_12(self, hour):
        instance = self.createInstance()
        instance.ampm = True
        instance.is_pm = mock.Mock(return_value=True)
        instance.hour = 12
        instance._padded_value = mock.Mock()
        instance.padded_hour()
        instance._padded_value.assert_called_with(12)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    def test_padded_minute_None(self, hour):
        instance = self.createInstance()
        instance.minute = None
        self.assertFalse(instance.padded_minute())

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    def test_padded_minute_not_None(self, hour):
        instance = self.createInstance()
        instance.minute = 55
        instance._padded_value = mock.Mock()
        instance.padded_minute()
        instance._padded_value.assert_called_with(55)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__year_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = None
        instance.month = 11
        instance.day = 22
        instance.hour = 23
        instance.minute = 55
        self.assertFalse(instance.js_value)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__month_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = None
        instance.day = 22
        instance.hour = 23
        instance.minute = 55
        self.assertFalse(instance.js_value)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__day_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = 11
        instance.day = None
        instance.hour = 23
        instance.minute = 55
        self.assertFalse(instance.js_value)

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__hour_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = 11
        instance.day = 22
        instance.hour = None
        instance.minute = 55
        self.assertEqual(
            instance.js_value,
            'new Date(2011, 10, 22), '
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__minute_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = 11
        instance.day = 22
        instance.hour = 23
        instance.minute = None
        self.assertEqual(
            instance.js_value,
            'new Date(2011, 10, 22), '
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.minute')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.hour')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDatetimeWidget.year')
    def test_js_value__datetime_not_None(self, year, month, day, hour, minute):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = 11
        instance.day = 22
        instance.hour = 23
        instance.minute = 55
        self.assertEqual(
            instance.js_value,
            'new Date(2011, 10, 22, 23, 55), '
        )
