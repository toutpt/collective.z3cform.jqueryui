from AccessControl import ClassSecurityInfo
from Products.Archetypes import Widget as widgets
from Products.Archetypes.Registry import registerWidget
from plone.formwidget.datetime import base


class DateWidget(base.AbstractDateWidget,
                 widgets.TypesWidget):
    """ Date widget.

    Please note: Archetypes DateTimeFields's values are Zope DateTime
    instances.

    """

    _properties = widgets.TypesWidget._properties.copy()
    _properties.update({
        'macro': 'date_input',
        'show_calendar': True,
        'show_day': True,
        'with_time': False,
    })

    security = ClassSecurityInfo()

    def __call__(self, mode, instance, context=None):
        self.context = instance
        self.request = instance.REQUEST
        return super(DateWidget, self).__call__(mode, instance, context=context)

    def _dtvalue(self, value):
        # part()[5] is seconds in float. casted to int by super
        return super(DateWidget, self)._dtvalue(value.parts()[:6])

    @property
    def name(self):
        return self.getName()

    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """Basic impl for form processing in a widget"""
        fname = field.getName()
        value = form.get("%s-calendar" % fname, empty_marker)
        if value is empty_marker:
            return empty_marker
        # If JS support is unavailable, the value
        # in the request may be missing or incorrect
        # since it won't have been assembled from the
        # input components. Instead of relying on it,
        # assemble the date/time from its input components.
        year = form.get('%s-year' % fname, '0000')
        month = form.get('%s-month' % fname, '00')
        day = form.get('%s-day' % fname, '00')
        hour = form.get('%s-hour' % fname, '00')
        minute = form.get('%s-min' % fname, '00')
        ampm = form.get('%s-ampm' % fname, '')
        if (year != '0000') and (day != '00') and (month != '00'):
            if ampm and ampm == 'PM' and hour != '12':
                hour = int(hour) + 12
            elif ampm and ampm == 'AM' and hour == '12':
                hour = '00'
            value = "%s-%s-%s %s:%s" % (year, month, day, hour, minute)
        else:
            value = ''
        if emptyReturnsMarker and value == '':
            return empty_marker
        # stick it back in request.form
        form[fname] = value
        return value, {}

registerWidget(DateWidget,
               title='Date widget',
               description=('Date widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )


class DatetimeWidget(base.AbstractDatetimeWidget,
                     DateWidget):
    """ DateTime widget """

    _properties = DateWidget._properties.copy()
    _properties.update({
        'macro': 'datetime_input',
        'with_time': True,
    })

registerWidget(DatetimeWidget,
               title='Datetime widget',
               description=('Datetime widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )


class MonthYearWidget(base.AbstractMonthYearWidget,
                      DateWidget):
    """ Month and year widget """

    _properties = DateWidget._properties.copy()
    _properties.update({
        'macro': 'monthyear_input',
        'show_day': False,
    })

registerWidget(MonthYearWidget,
               title='Month year widget',
               description=('Month year widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )
