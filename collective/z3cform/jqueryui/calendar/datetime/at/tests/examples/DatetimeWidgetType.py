from DateTime import DateTime

from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import BaseSchema
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import registerType
from Products.Archetypes.examples.SimpleType import SimpleType

from plone.formwidget.datetime.at import DateWidget
from plone.formwidget.datetime.at import DatetimeWidget
from plone.formwidget.datetime.at import MonthYearWidget


schema = BaseSchema.copy() + Schema((
    DateTimeField('datefield',
                  default_method=DateTime,
                  widget=DateWidget(
                      label='Date field',
                      description='',
                      )),
    DateTimeField('datetimefield',
                  default_method=DateTime,
                  widget=DatetimeWidget(
                      label='Datetime field',
                      description='',
                      ampm=1,
                      )),
    DateTimeField('monthyearfield',
                  default_method=DateTime,
                  widget=MonthYearWidget(
                      label='MonthYear field',
                      description='',
                      )),
    ))


class DatetimeWidgetType(SimpleType):
    """A simple archetype"""
    schema = schema
    archetype_name = meta_type = "DatetimeWidgetType"
    portal_type = 'DatetimeWidgetType'

registerType(DatetimeWidgetType, 'plone.formwidget.datetime.at.tests.examples')
