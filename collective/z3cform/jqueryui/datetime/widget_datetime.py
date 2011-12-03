#-*- coding: utf-8 -*- 

#############################################################################
#                                                                           #
#   Copyright (c) 2008 Rok Garbas <rok@garbas.si>                           #
#                                                                           #
# This program is free software; you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation; either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# This program is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                           #
#############################################################################
__docformat__ = "reStructuredText"

import z3c.form
import zope.schema
import zope.interface
import zope.component
from datetime import datetime
from widget_date import DateWidget
from interfaces import IDatetimeWidget

class DatetimeWidget(DateWidget):
    """ DateTime widget """

    zope.interface.implementsOnly(IDatetimeWidget)

    klass = u'datetime-widget'
    value = ('', '', '', '00', '00')
    ampm  = False

    @property
    def formatted_value(self):
        if self.value == ('', '', '', '00', '00'):
            return ''
        formatter = self.request.locale.dates.getFormatter("dateTime", "short")
        datetime_value = datetime(*map(int, self.value))
        if datetime_value.year > 1900:
            return formatter.format(datetime_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return datetime_value.ctime()

    @property
    def hour(self):
        hour = self.request.get(self.name+'-hour', None)
        if hour:
            return hour
        return self.value[3]

    @property
    def minute(self):
        min = self.request.get(self.name+'-min', None)
        if min:
            return min
        return self.value[4]

    def _padded_value(self, value):
        value = unicode(value)
        if value and len(value) == 1:
            value = u'0' + value
        return value

    def is_pm(self):
        if int(self.hour) >= 12:
            return True
        return False

    def padded_hour(self):
        hour = self.hour
        if self.ampm is True and self.is_pm() and int(hour)!=12:
            hour = str(int(hour)-12)
        return self._padded_value(hour)

    def padded_minute(self):
        return self._padded_value(self.minute)

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)
        hour = self.request.get(self.name + '-hour', default)
        minute = self.request.get(self.name + '-min', default)

        if default in (year, month, day, hour, minute):
            return default

        if self.ampm is True and int(hour)!=12:
            ampm = self.request.get(self.name + '-ampm', default)
            if ampm == 'PM':
                hour = str(12+int(hour))
            # something strange happened since we either
            # should have 'PM' or 'AM', return default
            elif ampm != 'AM':
                return default

        return (year, month, day, hour, minute)

@zope.component.adapter(zope.schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DatetimeFieldWidget(field, request):
    """IFieldWidget factory for DatetimeWidget."""
    return z3c.form.widget.FieldWidget(field, DatetimeWidget(request))

