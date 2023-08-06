====================
PyAMS fields package
====================

Introduction
------------

This package is composed of a set of components usable into any Pyramid application.
It relies on the PyAMS framework and can't be used without it.

The goal of this package is to allow a content manager to be able to define a set of
custom schema fields, which can be used to generate users forms automatically.

For example, the PyAMS_content CMS package defines a *form* shared content, which can
be used to define any kind of form (contact form, registry form...). However, how the
submitted data will be processed is not handled by this package: you can define any set
of *handlers* in your own applications; the only default form handler which is provided
by PyAMS_content will send data using an email address.


Site upgrade
------------

PyAMS_fields relies on other packages which are needing a site upgrade:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)
    >>> from pyams_form import includeme as include_form
    >>> include_form(config)

    >>> from pyams_fields import includeme as include_fields
    >>> include_fields(config)

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_site_before_traverse, get_local_registry
    >>> from pyams_site.generations import upgrade_site

    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...


Creating and using form fields
------------------------------

The first step is to create a container which will be able to receive form fields. This
container can be attached to a content implementing *IFormFieldsContainerTarget* interface:

    >>> from zope.interface import alsoProvides

    >>> from pyams_fields.interfaces import IFormFieldContainerTarget
    >>> alsoProvides(app, IFormFieldContainerTarget)

    >>> from pyams_fields.interfaces import IFormFieldContainer
    >>> container = IFormFieldContainer(app)
    >>> container
    <pyams_fields.container.FormFieldContainer object at 0x...>

Let's start by creating a first field:

    >>> from pyams_fields.field import FormField

    >>> field = FormField()
    >>> field.name = 'field1'
    >>> field.field_type = 'textline'
    >>> field.label = {'en': 'Field 1'}

    >>> field.get_field_factory()
    <pyams_fields.field.TextLineFieldFactory object at 0x...>

    >>> container[field.name] = field

    >>> list(container.keys())
    ['field1']
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>]

    >>> list(container.find_fields('textline'))
    [<pyams_fields.field.FormField object at 0x...>]

Form fields target provides traverser and sublocations to get access to fields container:

    >>> from zope.traversing.interfaces import ITraversable

    >>> traverser = request.registry.queryAdapter(app, ITraversable, name='fields')
    >>> traverser.traverse('') is container
    True
    >>> traverser.traverse('field1') is field
    True

    >>> from zope.location.interfaces import ISublocations
    >>> locations = request.registry.queryAdapter(app, ISublocations, name='fields')
    >>> list(locations.sublocations())
    [<pyams_fields.field.FormField object at 0x...>]


Form fields permission checker
------------------------------

Form fields container get their permission checker from their context:

    >>> from pyams_security.interfaces import IViewContextPermissionChecker

    >>> try:
    ...     checker = request.registry.queryAdapter(field, IViewContextPermissionChecker)
    ... except TypeError:
    ...     checker = None

    >>> checker is None
    True

This error is due to the fact that we actually don't have a permission checker on site root!
Let's create one:

    >>> from pyams_utils.adapter import ContextAdapter
    >>> from pyams_site.interfaces import ISiteRoot

    >>> class SiteRootAdapter(ContextAdapter):
    ...     edit_permission = 'edit'

    >>> request.registry.registerAdapter(SiteRootAdapter, (ISiteRoot,), IViewContextPermissionChecker)

    >>> checker = request.registry.queryAdapter(field, IViewContextPermissionChecker)
    >>> checker
    <pyams_fields.tests.test_utilsdocs.SiteRootAdapter object at 0x...>
    >>> checker.context is app
    True

    >>> checker.edit_permission
    'edit'


Custom form fields
------------------

Choice and List fields require a custom schema field factory and a set of selection values:

    >>> field2 = FormField()
    >>> field2.name = 'field2'
    >>> field2.field_type = 'choice'
    >>> field2.label = {'en': 'Field 2'}
    >>> field2.values = ["Value 1", "Value 2"]

    >>> container['field2'] = field2
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>, <zope.schema._field.Choice object at 0x... field2>]

    >>> field3 = FormField()
    >>> field3.name = 'field3'
    >>> field3.field_type = 'list'
    >>> field3.label = {'en': 'Field 3'}
    >>> field3.values = ["Value 1", "Value 2"]

    >>> field2.visible = False

    >>> container['field3'] = field3
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>, <zope.schema._field.List object at 0x... field3>]
    >>> list(container.find_fields('choice'))
    []


Tests cleanup:

    >>> tearDown()
