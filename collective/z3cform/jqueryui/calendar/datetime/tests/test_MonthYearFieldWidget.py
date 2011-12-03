import mock
import unittest2 as unittest


class TestMonthYearFieldWidget(unittest.TestCase):

    @mock.patch('plone.formwidget.datetime.z3cform.widget.MonthYearWidget')
    @mock.patch('plone.formwidget.datetime.z3cform.widget.z3c.form.widget.FieldWidget')
    def test_MonthYearFieldWidget(self, FieldWidget, MonthYearWidget):
        from plone.formwidget.datetime.z3cform.widget import MonthYearFieldWidget
        field = mock.Mock()
        request = mock.Mock()
        MonthYearFieldWidget(field, request)
        self.assertTrue(FieldWidget.called)
        self.assertTrue(MonthYearWidget.called)
