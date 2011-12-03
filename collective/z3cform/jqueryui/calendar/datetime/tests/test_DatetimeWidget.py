import mock
import unittest2 as unittest


class TestDatetimeWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.widget import DatetimeWidget
        instance = DatetimeWidget(mock.Mock())
        instance.name = 'field'
        return instance

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.widget import DatetimeWidget
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        self.assertTrue(
            issubclass(
                DatetimeWidget,
                (
                    AbstractDatetimeWidget,
                    DateWidget,
                )
            )
        )

    def test_instance_provides__default_not_in_(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.interfaces import IDatetimeWidget
        self.assertTrue(IDatetimeWidget.providedBy(instance))

    def test_extract(self):
        instance = self.createInstance()
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
            'field-hour': '5',
            'field-min': '30',
        }
        self.assertEqual(
            instance.extract(),
            ('2011', '11', '21', '5', '30')
        )

    def test_extract__default_in_(self):
        instance = self.createInstance()
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
            'field-hour': '5',
            'field-min': '30',
        }
        default = mock.Mock()
        self.assertEqual(
            instance.extract(default),
            ('2011', '11', '21', '5', '30')
        )

    def test_extract__ampm_am(self):
        instance = self.createInstance()
        instance.ampm = True
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
            'field-hour': '5',
            'field-min': '30',
            'field-ampm': 'AM'
        }
        self.assertEqual(
            instance.extract(),
            ('2011', '11', '21', '5', '30')
        )

    def test_extract__ampm_pm(self):
        instance = self.createInstance()
        instance.ampm = True
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
            'field-hour': '5',
            'field-min': '30',
            'field-ampm': 'PM'
        }
        self.assertEqual(
            instance.extract(),
            ('2011', '11', '21', '17', '30')
        )

    def test_extract__ampm_ampm(self):
        instance = self.createInstance()
        instance.ampm = True
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
            'field-hour': '5',
            'field-min': '30',
            'field-ampm': 'AMPM'
        }
        self.assertEqual(
            instance.extract('default'),
            'default'
        )

    @mock.patch('plone.formwidget.datetime.z3cform.widget.DatetimeWidget._dtformatter')
    def test_extract__default_in_with_error(self, _dtformatter):
        instance = self.createInstance()
        instance.request = mock.MagicMock()
        default = instance.request.get('field-day')
        from zope.i18n.format import DateTimeParseError
        instance._dtformatter.parse = mock.Mock(side_effect=DateTimeParseError)
        self.assertEqual(instance.extract(default), default)

    def test_extract__default_in_without_error(self):
        instance = self.createInstance()
        instance.request = mock.MagicMock()
        day = instance.request.get('field-day')
        self.assertEqual(
            len(instance.extract(day)),
            5
        )
