import mock
import unittest2 as unittest


class TestAbstractDateWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.base import AbstractDateWidget
        return AbstractDateWidget()

    def test_instance__calendar_type(self):
        instance = self.createInstance()
        self.assertEqual(instance.calendar_type, 'gregorian')

    def test_instance__klass(self):
        instance = self.createInstance()
        self.assertEqual(instance.klass, u'date-widget')

    def test_instance__empty_value(self):
        instance = self.createInstance()
        self.assertEqual(instance.empty_value, ('', '', ''))

    def test_instance__value(self):
        instance = self.createInstance()
        self.assertEqual(instance.value, ('', '', ''))

    def test_instance__show_today_link(self):
        instance = self.createInstance()
        self.assertFalse(instance.show_today_link)

    def test_instance__show_jquerytools_dateinput(self):
        instance = self.createInstance()
        self.assertFalse(instance.show_jquerytools_dateinput)

    def test_instance__jquerytools_dateinput_config(self):
        instance = self.createInstance()
        self.assertEqual(
            instance.jquerytools_dateinput_config,
            'selectors: true, ' \
            'trigger: true, ' \
            'yearRange: [-10, 10]'
        )

    def test_instance__popup_calendar_icon(self):
        instance = self.createInstance()
        self.assertEqual(
            instance.popup_calendar_icon,
            ".css({'width': '16px', 'vertical-align': 'middle', 'display': 'inline-block', 'background': 'url(popup_calendar.gif)', 'height': '16px'})"
        )

    def test__dtformatter(self):
        instance = self.createInstance()
        getFormatter = mock.Mock()
        instance.request = mock.Mock()
        instance.request.locale.dates.getFormatter = getFormatter
        instance._dtformatter
        getFormatter.assert_called_with('date', 'short')

    @mock.patch('plone.formwidget.datetime.base.date')
    def test__dtvalue(self, date):
        instance = self.createInstance()
        value = '123'
        instance._dtvalue(value)
        date.assert_called_with(1, 2, 3)

    def test_formatted_value__value_in_empty_value(self):
        instance = self.createInstance()
        self.assertFalse(instance.formatted_value)

    def test_formatted_value__value_is_None(self):
        instance = self.createInstance()
        instance.value = None
        self.assertFalse(instance.formatted_value)

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget._dtformatter')
    def test_formatted_value__year_more_than_1900(self, _dtformatter):
        instance = self.createInstance()
        instance.value = mock.Mock()
        instance._dtvalue = mock.Mock()
        dt_value = instance._dtvalue()
        dt_value.year = 2011
        instance.formatted_value
        _dtformatter.format.assert_called_with(dt_value)

    def test_formatted_value__year_is_1900(self):
        instance = self.createInstance()
        instance.value = mock.Mock()
        instance._dtvalue = mock.Mock()
        dt_value = instance._dtvalue()
        dt_value.year = 1900
        instance.formatted_value
        self.assertTrue(dt_value.ctime.called)

    def test_years(self):
        instance = self.createInstance()
        self.assertEqual(len(instance.years), 20)
        self.assertEqual(
            instance.years[0],
            {'name': 2000, 'value': 2000}
        )
        self.assertEqual(
            instance.years[19],
            {'name': 2019, 'value': 2019}
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.month')
    def test_months_selected(self, month):
        instance = self.createInstance()
        instance.month = '3'
        instance.request = mock.Mock()
        calendar_type = mock.Mock()
        calendar = mock.Mock()
        instance.calendar_type = calendar_type
        instance.request.locale.dates.calendars = {calendar_type: calendar}
        calendar.getMonthNames.return_value = ['Jan', 'Feb', 'Mar', 'Apr']
        self.assertEqual(
            [month for month in instance.months],
            [
                {'selected': False, 'name': 'Jan', 'value': 1},
                {'selected': False, 'name': 'Feb', 'value': 2},
                {'selected': True, 'name': 'Mar', 'value': 3},
                {'selected': False, 'name': 'Apr', 'value': 4}
            ]
        )

    def test_months_unselected(self):
        instance = self.createInstance()
        instance.request = mock.Mock()
        calendar_type = mock.Mock()
        calendar = mock.Mock()
        instance.calendar_type = calendar_type
        instance.request.locale.dates.calendars = {calendar_type: calendar}
        calendar.getMonthNames.return_value = ['Jan', 'Feb', 'Mar', 'Apr']
        self.assertEqual(
            [month for month in instance.months],
            [
                {'selected': False, 'name': 'Jan', 'value': 1},
                {'selected': False, 'name': 'Feb', 'value': 2},
                {'selected': False, 'name': 'Mar', 'value': 3},
                {'selected': False, 'name': 'Apr', 'value': 4}
            ]
        )

    def test_days(self):
        instance = self.createInstance()
        self.assertEqual(len(instance.days), 31)
        self.assertEqual(instance.days[0], {'name': '01', 'value': 1})
        self.assertEqual(instance.days[-1], {'name': '31', 'value': 31})

    def test_year_is_not_None(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = '2011'
        self.assertEqual(instance.year, '2011')

    def test_year_is_None_value_not_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '123'
        instance.empty_value = '456'
        self.assertEqual(instance.year, '1')

    def test_year_is_None_value_is_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '123'
        instance.empty_value = '145'
        self.assertFalse(instance.year)

    def test_month_is_not_None(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = '11'
        self.assertEqual(instance.month, '11')

    def test_month_is_None_value_not_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '123'
        instance.empty_value = '456'
        self.assertEqual(instance.month, '2')

    def test_month_is_None_value_is_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '143'
        instance.empty_value = '145'
        self.assertFalse(instance.month)

    def test_day_is_not_None(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = '31'
        self.assertEqual(instance.day, '31')

    def test_day_is_None_value_not_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '123'
        instance.empty_value = '456'
        self.assertEqual(instance.day, '3')

    def test_day_is_None_value_is_empty_value(self):
        instance = self.createInstance()
        instance.name = 'field'
        instance.request = {}
        instance.value = '125'
        instance.empty_value = '345'
        self.assertFalse(instance.day)

    def test__padded_value__empty(self):
        instance = self.createInstance()
        value = ''
        self.assertEqual(instance._padded_value(value), '00')

    def test__padded_value__one(self):
        instance = self.createInstance()
        value = 'a'
        self.assertEqual(instance._padded_value(value), '0a')

    def test__padded_value__two(self):
        instance = self.createInstance()
        value = 'ab'
        self.assertEqual(instance._padded_value(value), 'ab')

    def test__padded_value__three(self):
        instance = self.createInstance()
        value = 'abc'
        self.assertEqual(instance._padded_value(value), 'abc')

    @mock.patch('plone.formwidget.datetime.zope.i18n.translate')
    @mock.patch('plone.formwidget.datetime.base.datetime')
    def test_show_today_link_js(self, datetime, translate):
        instance = self.createInstance()
        instance.id = 'id'
        now = datetime.today()
        now.day = 22
        now.month = 11
        now.year = 2011
        instance.request = mock.Mock()
        translate.return_value = 'Today'
        self.assertEqual(
            instance.show_today_link_js(),
            '<a href="#" onclick="document.getElementById(\'id-day\').value = 22;document.getElementById(\'id-month\').value = 11;document.getElementById(\'id-year\').value = 2011;return false;">Today</a>'
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.year')
    def test_js_value_date_None(self, year, month, day):
        instance = self.createInstance()
        instance.year = None
        instance.month = None
        instance.day = None
        self.assertFalse(instance.js_value)

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.day')
    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.month')
    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.year')
    def test_js_value_date_not_None(self, year, month, day):
        instance = self.createInstance()
        instance.year = 2011
        instance.month = 11
        instance.day = 22
        self.assertEqual(
            instance.js_value,
            'new Date(2011, 10, 22), '
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.js_value')
    def test_get_js__js_value_None(self, js_value):
        instance = self.createInstance()
        instance.id = 'id'
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = 'en'
        calendar_type = mock.Mock()
        instance.calendar_type = calendar_type
        calendar = mock.Mock()
        instance.request.locale.dates.calendars = {instance.calendar_type: calendar}
        calendar.getMonthNames.return_value = ['Jan', 'Feb', 'Mar', 'Apr']
        calendar.getMonthAbbreviations.return_value = ['J', 'F', 'M', 'A']
        calendar.getDayNames.return_value = ['Mon', 'Tue', 'Wed']
        calendar.getDayAbbreviations.return_value = ['M', 'T', 'W']
        instance.js_value = None
        self.assertEqual(
            instance.get_js(),
            '\n            <input type="hidden"\n                id="id-calendar"\n                name="field-calendar"\n                class="field-calendar" />\n            <script type="text/javascript">\n                if (jQuery().dateinput) {\n                    jQuery.tools.dateinput.localize("en", {months: "Jan,Feb,Mar,Apr",shortMonths: "J,F,M,A",days: "Mon,Tue,Wed",shortDays: "M,T,W",});\n                    jQuery("#id-calendar").dateinput({lang: "en", change: function() {\n  var value = this.getValue("yyyy-mm-dd").split("-");\n  jQuery("#id-year").val(value[0]); \n  jQuery("#id-month").val(value[1]); \n  jQuery("#id-day").val(value[2]); \n}, selectors: true, trigger: true, yearRange: [-10, 10]}).unbind(\'change\')\n                        .bind(\'onShow\', function (event) {\n                            var trigger_offset = jQuery(this).next().offset();\n                            jQuery(this).data(\'dateinput\').getCalendar().offset(\n                                {top: trigger_offset.top+20, left: trigger_offset.left}\n                            );\n                        });\n                    jQuery("#id-calendar").next().css({\'width\': \'16px\', \'vertical-align\': \'middle\', \'display\': \'inline-block\', \'background\': \'url(popup_calendar.gif)\', \'height\': \'16px\'});\n                }\n            </script>'
        )

    @mock.patch('plone.formwidget.datetime.base.AbstractDateWidget.js_value')
    def test_get_js__js_value(self, js_value):
        instance = self.createInstance()
        instance.id = 'id'
        instance.name = 'field'
        instance.request = mock.Mock()
        instance.request.get.return_value = 'en'
        calendar_type = mock.Mock()
        instance.calendar_type = calendar_type
        calendar = mock.Mock()
        instance.request.locale.dates.calendars = {instance.calendar_type: calendar}
        calendar.getMonthNames.return_value = ['Jan', 'Feb', 'Mar', 'Apr']
        calendar.getMonthAbbreviations.return_value = ['J', 'F', 'M', 'A']
        calendar.getDayNames.return_value = ['Mon', 'Tue', 'Wed']
        calendar.getDayAbbreviations.return_value = ['M', 'T', 'W']
        instance.js_value = 'js_value'
        instance.jquerytools_dateinput_config = 'jquerytools_dateinput_config'
        self.assertEqual(
            instance.get_js(),
            '\n            <input type="hidden"\n                id="id-calendar"\n                name="field-calendar"\n                class="field-calendar" />\n            <script type="text/javascript">\n                if (jQuery().dateinput) {\n                    jQuery.tools.dateinput.localize("en", {months: "Jan,Feb,Mar,Apr",shortMonths: "J,F,M,A",days: "Mon,Tue,Wed",shortDays: "M,T,W",});\n                    jQuery("#id-calendar").dateinput({lang: "en", value: js_value, change: function() {\n  var value = this.getValue("yyyy-mm-dd").split("-");\n  jQuery("#id-year").val(value[0]); \n  jQuery("#id-month").val(value[1]); \n  jQuery("#id-day").val(value[2]); \n}, jquerytools_dateinput_config}).unbind(\'change\')\n                        .bind(\'onShow\', function (event) {\n                            var trigger_offset = jQuery(this).next().offset();\n                            jQuery(this).data(\'dateinput\').getCalendar().offset(\n                                {top: trigger_offset.top+20, left: trigger_offset.left}\n                            );\n                        });\n                    jQuery("#id-calendar").next().css({\'width\': \'16px\', \'vertical-align\': \'middle\', \'display\': \'inline-block\', \'background\': \'url(popup_calendar.gif)\', \'height\': \'16px\'});\n                }\n            </script>'
        )
