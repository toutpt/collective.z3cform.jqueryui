import unittest2 as unittest


class TestDatetimeWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.at.widget import DatetimeWidget
        return DatetimeWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.at.widget import DatetimeWidget
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        from plone.formwidget.datetime.at.widget import DateWidget
        self.assertTrue(DatetimeWidget, (AbstractDatetimeWidget, DateWidget))

    def test__properties(self):
        instance = self.createInstance()
        self.assertEqual(
            instance._properties,
            {
                'show_calendar': True,
                'helper_css': (),
                'with_time': True,
                'description': '',
                'populate': True,
                'show_day': True,
                'macro': 'datetime_input',
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
