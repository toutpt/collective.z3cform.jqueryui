from plone.z3cform import layout
from Products.CMFCore.utils import getToolByName
from z3c.form import form, button, field
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import adapts
from zope.interface import Interface, implements
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from collective.z3cform.jqueryui import DateWidget
from collective.z3cform.jqueryui import DateFieldWidget
from collective.z3cform.jqueryui import DatetimeWidget
from collective.z3cform.jqueryui import DatetimeFieldWidget
from collective.z3cform.jqueryui import MonthYearWidget
from collective.z3cform.jqueryui import MonthYearFieldWidget


class ITestForm(Interface):

    date = schema.Date(title=u"Date", required=False)
    datetime = schema.Datetime(title=u"Date time", required=False)

from datetime import date, datetime

class TestAdapter(object):
    implements(ITestForm)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def _get_date(self):
        return date.today()

    def _set_date(self, value):
        print "setting", value

    date = property(_get_date, _set_date)

    def _get_datetime(self):
        return datetime.today()

    def _set_datetime(self, value):
        print "setting", value

    datetime = property(_get_datetime, _set_datetime)


class TestForm(form.Form):
    fields = field.Fields(ITestForm)
    fields['date'].widgetFactory = DateFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

TestView = layout.wrap_form(TestForm)
