#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_fields.interfaces module

"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Interface
from zope.location.interfaces import IContained
from zope.schema import Bool, TextLine, Choice

from pyams_i18n.schema import I18nTextLineField, I18nTextField
from pyams_utils.schema import TextLineListField

from pyams_fields import _


PYAMS_FIELDS_TYPES = 'pyams_fields.types'

PYAMS_FIELDS_CONTAINER_KEY = 'pyams_fields.container'


class IFormField(IContained, IAttributeAnnotatable):
    """Form field interface"""

    containers('.IFormFieldContainer')

    name = TextLine(title=_("Field name"),
                    description=_("Field internal name; must be unique for a given form"),
                    required=True)

    field_type = Choice(title=_("Field type"),
                        description=_("Selected field type"),
                        vocabulary=PYAMS_FIELDS_TYPES,
                        required=True)

    label = I18nTextLineField(title=_("Label"),
                              description=_("User field label"),
                              required=True)

    description = I18nTextField(title=_("Description"),
                                description=_("Field description can be displayed as hint"),
                                required=False)

    placeholder = TextLine(title=_("Placeholder"),
                           description=_("Some field types like text line can display a "
                                         "placeholder"),
                           required=False)

    values = TextLineListField(title=_("Optional values"),
                               description=_("List of available values (for 'choice' and 'list' "
                                             "field types)"),
                               required=False)

    default = I18nTextLineField(title=_("Default value"),
                                description=_("Give default value if field type can use it"),
                                required=False)

    required = Bool(title=_("Required?"),
                    description=_("Select 'yes' to set field as mandatory"),
                    required=True,
                    default=False)

    visible = Bool(title=_("Visible?"),
                   description=_("Select 'no' to hide given field..."),
                   required=True,
                   default=True)


class IFormFieldFactory(Interface):
    """Form field factory interface"""

    label = Attribute("Factory label")
    weight = Attribute("Factory weight")

    def get_schema_field(self, field):
        """Get schema field matching given form field"""


class IFormFieldDataConverter(Interface):
    """Interface of a converter adapter which can be used to convert form data"""

    def convert(self, value):
        """Convert given input value"""


class IFormFieldContainer(IContainer):
    """Form fields container interface"""

    contains(IFormField)

    def append(self, field):
        """Append given field to container"""

    def get_fields(self):
        """Get schema fields matching current fields"""

    def find_fields(self, factory):
        """Find fields matching given factory (defined by its utility name)"""


class IFormFieldContainerTarget(IAttributeAnnotatable):
    """Form fields container target marker interface"""
