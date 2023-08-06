# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Layout(Component):
    """A Layout component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Main content.

- className (string; optional):
    Layout wrapper className.

- drawerContent (a list of or a singular dash component, string or number; optional):
    Contents of drawer.

- headerContent (a list of or a singular dash component, string or number; optional):
    Contents of header.

- open (boolean; optional):
    Signifies if drawer of Layout is open.

- showLeftHandNav (boolean; optional):
    Toggle off and on the drawer and sidebar.

- sidebarContent (a list of or a singular dash component, string or number; optional):
    Contents of sidebar."""
    _children_props = ['drawerContent', 'headerContent', 'sidebarContent']
    _base_nodes = ['drawerContent', 'headerContent', 'sidebarContent', 'children']
    _namespace = 'ea_dash'
    _type = 'Layout'
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, drawerContent=Component.UNDEFINED, headerContent=Component.UNDEFINED, sidebarContent=Component.UNDEFINED, open=Component.UNDEFINED, showLeftHandNav=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'className', 'drawerContent', 'headerContent', 'open', 'showLeftHandNav', 'sidebarContent']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'className', 'drawerContent', 'headerContent', 'open', 'showLeftHandNav', 'sidebarContent']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Layout, self).__init__(children=children, **args)
