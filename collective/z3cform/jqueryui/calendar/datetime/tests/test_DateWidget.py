import mock
import unittest2 as unittest


class TestDateWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        instance = DateWidget(mock.Mock())
        instance.name = 'field'
        return instance

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        from z3c.form.browser.widget import HTMLTextInputWidget
        from z3c.form.widget import Widget
        self.assertTrue(
            DateWidget,
            (
               AbstractDateWidget,
               HTMLTextInputWidget,
               Widget,
            )
        )

    def test_instance_provides(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.interfaces import IDateWidget
        self.assertTrue(IDateWidget.providedBy(instance))

    ## Testing update call from the super class is missing.
    @mock.patch('plone.formwidget.datetime.z3cform.widget.z3c.form.browser.widget.addFieldClass')
    def test_update(self, addFieldClass):
        instance = self.createInstance()
        instance.update()
        self.assertTrue(addFieldClass.called)

    def test_extract__default_not_in_(self):
        instance = self.createInstance()
        instance.request = {
            'field-day': '21',
            'field-month': '11',
            'field-year': '2011',
        }
        self.assertEqual(
            instance.extract(),
            ('2011', '11', '21')
        )

    @mock.patch('plone.formwidget.datetime.z3cform.widget.DateWidget._dtformatter')
    def test_extract__default_in_with_error(self, _dtformatter):
        instance = self.createInstance()
        instance.request = mock.MagicMock()
        day = instance.request.get('field-day')
        from zope.i18n.format import DateTimeParseError
        instance._dtformatter.parse = mock.Mock(side_effect=DateTimeParseError)
        self.assertEqual(instance.extract(day), day)

    def test_extract__default_in_without_error(self):
        instance = self.createInstance()
        instance.request = mock.MagicMock()
        day = instance.request.get('field-day')
        self.assertEqual(len(instance.extract(day)), 3)

    def test_js_value__without_empty_string_in_value(self):
        instance = self.createInstance()
        instance.value = ('2011', '11', '21')
        self.assertEqual(
            instance.js_value,
            'value: new Date(2011, 11, 21), '
        )

    def test_js_value__with_empty_string_in_value(self):
        instance = self.createInstance()
        instance.value = ('', '11', '21')
        self.assertEqual(instance.js_value, '')
