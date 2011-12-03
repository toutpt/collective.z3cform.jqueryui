import z3c.form
import z3c.form.interfaces
import zope.schema

from plone.formwidget.datetime import MessageFactory as _


# Fields

class IDateField(zope.schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


class IDatetimeField(zope.schema.interfaces.IDatetime):
    """ Special marker for datetime fields that use our widget """


# Widgets

class IDateWidget(z3c.form.interfaces.IWidget):
    """ Date widget marker for z3c.form """

    show_today_link = zope.schema.Bool(
        title=u'Show "today" link',
        description=(u'show a link that uses javascript to inserts '
                     u'the current date into the widget.'),
        default=False,
        )


class IDatetimeWidget(z3c.form.interfaces.IWidget):
    """ Datetime widget marker for z3c.form """


class IMonthYearWidget(z3c.form.interfaces.IWidget):
    """ MonthYear widget marker for z3c.form """


# Errors

class DateValidationError(zope.schema.ValidationError):
    __doc__ = _(u'Please enter a valid date.')


class DatetimeValidationError(zope.schema.ValidationError):
    __doc__ = _(u'Please enter a valid date and time.')
