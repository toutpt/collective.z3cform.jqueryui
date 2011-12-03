import mock
import unittest2 as unittest


class TestDateFieldWidget(unittest.TestCase):

    @mock.patch('plone.formwidget.datetime.z3cform.widget.DateWidget')
    @mock.patch('plone.formwidget.datetime.z3cform.widget.z3c.form.widget.FieldWidget')
    def test_DateFieldWidget(self, FieldWidget, DateWidget):
        from plone.formwidget.datetime.z3cform.widget import DateFieldWidget
        field = mock.Mock()
        request = mock.Mock()
        DateFieldWidget(field, request)
        self.assertTrue(FieldWidget.called)
        self.assertTrue(DateWidget.called)
