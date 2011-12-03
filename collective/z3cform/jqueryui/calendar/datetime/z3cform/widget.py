from interfaces import IDateWidget
from interfaces import IDatetimeWidget
from interfaces import IMonthYearWidget
from plone.formwidget.datetime import base

import z3c.form
import z3c.form.browser.widget
import z3c.form.widget
import zope.component
import zope.i18n
import zope.interface
import zope.schema


class DateWidget(base.AbstractDateWidget,
                 z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """ Date widget.

    Please note: zope.schema date/datetime field values are python datetime
    instances.

    """
    zope.interface.implementsOnly(IDateWidget)

    def update(self):
        super(DateWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)

        if not default in (year, month, day):
            return (year, month, day)

        # get a hidden value
        formatter = self._dtformatter
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day))
        except zope.i18n.format.DateTimeParseError:
            pass

        return default

    @property
    def js_value(self):
        value_date = self.value[:3]
        if '' not in value_date:
            return 'value: new Date(%s, %s, %s), ' % (value_date)
        else:
            return ''


@zope.component.adapter(zope.schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return z3c.form.widget.FieldWidget(field, DateWidget(request))


class DatetimeWidget(base.AbstractDatetimeWidget,
                     DateWidget):
    """ DateTime widget """
    zope.interface.implementsOnly(IDatetimeWidget)

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)
        hour = self.request.get(self.name + '-hour', default)
        minute = self.request.get(self.name + '-min', default)

        if (self.ampm is True and
            hour is not default and
            minute is not default and
            int(hour)!=12):
            ampm = self.request.get(self.name + '-ampm', default)
            if ampm == 'PM':
                hour = str(12+int(hour))
            # something strange happened since we either
            # should have 'PM' or 'AM', return default
            elif ampm != 'AM':
                return default

        if default not in (year, month, day, hour, minute):
            return (year, month, day, hour, minute)

        # get a hidden value
        formatter = self._dtformatter
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day),
                    str(dateobj.hour),
                    str(dateobj.minute))
        except zope.i18n.format.DateTimeParseError:
            pass

        return default


@zope.component.adapter(zope.schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DatetimeFieldWidget(field, request):
    """IFieldWidget factory for DatetimeWidget."""
    return z3c.form.widget.FieldWidget(field, DatetimeWidget(request))


class MonthYearWidget(base.AbstractMonthYearWidget,
                      DateWidget):
    """ Month and year widget """
    zope.interface.implementsOnly(IMonthYearWidget)


@zope.component.adapter(zope.schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def MonthYearFieldWidget(field, request):
    """IFieldWidget factory for MonthYearWidget."""
    return z3c.form.widget.FieldWidget(field, MonthYearWidget(request))
