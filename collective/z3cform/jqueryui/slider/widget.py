import json

from zope import component
from zope import interface
from zope.schema.interfaces import IInt

import z3c.form
from z3c.form.browser import widget, text
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer

from collective.z3cform.jqueryui import interfaces


class SliderWidget(text.TextWidget):
    """ Slider widget. """

    maxlength = 7
    size = 8
    readonly = True

    interface.implementsOnly(interfaces.ISliderWidget)
#    klass = u'jqueryui-slider-widget'


    options = dict(
        disabled                = False,
        animate_bool            = False,
        animate_string          = None,
        animate_number          = None,
        operation               = "horizontal", #or vertical
        step                    = 1)

#    def update(self):
#        super(SliderWidget, self).update()
#        widget.addFieldClass(self)

    def compile_options(self):
        return json.dumps(self.options)

    def slider_javascript(self):
        return '''/* <![CDATA[ */
            $(document).ready(function(){
                slider = $("#%(id)s").slider(%(options)s);
            });
            /* ]]> */''' % dict(id=self.id,
                                options=self.compile_options())

    def display_js(self):
        return '''/* <![CDATA[ */
            $(document).ready(function(){
                slider = $("#%(id)s").progressbar({value:%(value)s);
            });
            /* ]]> */''' % dict(id=self.id,
                                value=self.value)


def SliderFieldWidget(field, request):
   """IFieldWidget factory for SliderFieldWidget."""
   return FieldWidget(field, SliderWidget(request))

#from z3c.form import converter
#
#class IntConverter(converter.IntegerDataConverter):
#    """A special data converter for integer."""
#
#    component.adapts(IInt, interfaces.ISliderWidget)
