import mock
import unittest2 as unittest


class TestDatetimeFieldWidget(unittest.TestCase):

    @mock.patch('plone.formwidget.datetime.z3cform.widget.DatetimeWidget')
    @mock.patch('plone.formwidget.datetime.z3cform.widget.z3c.form.widget.FieldWidget')
    def test_DatetimeFieldWidget(self, FieldWidget, DatetimeWidget):
        from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
        field = mock.Mock()
        request = mock.Mock()
        DatetimeFieldWidget(field, request)
        self.assertTrue(FieldWidget.called)
        self.assertTrue(DatetimeWidget.called)
