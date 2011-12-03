import mock
import unittest2 as unittest


class TestDateWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.at.widget import DateWidget
        return DateWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.at.widget import DateWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        from Products.Archetypes.Widget import TypesWidget
        self.assertTrue(DateWidget, (AbstractDateWidget, TypesWidget))

    def test__properties(self):
        instance = self.createInstance()
        self.assertEqual(
            instance._properties,
            {
                'show_calendar': True,
                'helper_css': (),
                'with_time': False,
                'description': '',
                'populate': True,
                'show_day': True,
                'macro': 'date_input',
                'postback': True,
                'label': '',
                'visible': {'edit': 'visible', 'view': 'visible'},
                'blurrable': False,
                'modes': ('view', 'edit'),
                'show_content_type': False,
                'condition': '',
                'helper_js': ()
            }
        )

    def test__call_(self):
        instance = self.createInstance()
        mode = mock.Mock()
        ins = mock.MagicMock()
        request = mock.Mock()
        ins.REQUEST = request
        instance(mode, ins)

    def test__dtvalue(self):
        instance = self.createInstance()
        value = mock.Mock()
        value.parts.return_value = '123'
        instance._dtvalue(value)

    def test_name(self):
        instance = self.createInstance()
        instance.getName = mock.Mock(return_value='name')
        self.assertTrue(instance.name, 'name')

    def test_process_form_value_is_empty(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        form = {}
        self.assertFalse(instance.process_form(ins, field, form))

    def test_process_form_with_invalid_date_emptyReturnsMarker_False(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': None,
        }
        self.assertEqual(
            instance.process_form(ins, field, form),
            ('', {})
        )
        self.assertFalse(form['field'])

    def test_process_form_with_invalid_date_emptyReturnsMarker_True(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': None,
        }
        self.assertFalse(
            instance.process_form(ins, field, form, emptyReturnsMarker=True)
        )

    def test_process_form_with_valid_date_without_time(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': '2011',
            'field-month': '11',
            'field-day': '22',
        }
        self.assertEqual(
            instance.process_form(ins, field, form),
            ('2011-11-22 00:00', {})
        )
        self.assertEqual(
            form['field'],
            '2011-11-22 00:00'
        )

    def test_process_form_with_valid_date_without_ampm(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': '2011',
            'field-month': '11',
            'field-day': '22',
            'field-hour': '13',
            'field-min': '30',
        }
        self.assertEqual(
            instance.process_form(ins, field, form),
            ('2011-11-22 13:30', {})
        )
        self.assertEqual(
            form['field'],
            '2011-11-22 13:30'
        )

    def test_process_form_with_valid_date_pm(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': '2011',
            'field-month': '11',
            'field-day': '22',
            'field-hour': '2',
            'field-min': '30',
            'field-ampm': 'PM',
        }
        self.assertEqual(
            instance.process_form(ins, field, form),
            ('2011-11-22 14:30', {})
        )
        self.assertEqual(
            form['field'],
            '2011-11-22 14:30'
        )

    def test_process_form_with_valid_date_am(self):
        instance = self.createInstance()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field-calendar': 'value',
            'field-year': '2011',
            'field-month': '11',
            'field-day': '22',
            'field-hour': '12',
            'field-min': '30',
            'field-ampm': 'AM',
        }
        self.assertEqual(
            instance.process_form(ins, field, form),
            ('2011-11-22 00:30', {})
        )
        self.assertEqual(
            form['field'],
            '2011-11-22 00:30'
        )
