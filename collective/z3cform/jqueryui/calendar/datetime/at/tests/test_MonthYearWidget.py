import unittest2 as unittest


class TestMonthYearWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.at.widget import MonthYearWidget
        return MonthYearWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.at.widget import MonthYearWidget
        from plone.formwidget.datetime.base import AbstractMonthYearWidget
        from plone.formwidget.datetime.at.widget import DateWidget
        self.assertTrue(MonthYearWidget, (AbstractMonthYearWidget, DateWidget))

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
                'show_day': False,
                'macro': 'monthyear_input',
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
