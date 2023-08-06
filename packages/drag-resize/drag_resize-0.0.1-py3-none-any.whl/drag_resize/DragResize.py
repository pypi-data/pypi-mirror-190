# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DragResize(Component):
    """A DragResize component.


Keyword arguments:

- children (dict; optional)

- id (string; optional)

- h (string; optional)

- w (string; optional)

- x (number; optional)

- y (number; optional)"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, w=Component.UNDEFINED, h=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'h', 'w', 'x', 'y']
        self._type = 'DragResize'
        self._namespace = 'drag_resize'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'h', 'w', 'x', 'y']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DragResize, self).__init__(children=children, **args)
