# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DragDash(Component):
    """A DragDash component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    .

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- axis (string; optional):
    .

- defaultPosition (dict; optional):
    .

- deltaX (number; optional):
    .

- deltaY (number; optional):
    .

- disabled (boolean; optional):
    .

- grid (list; optional):
    .

- handle (string; optional):
    .

- ismoved (boolean; optional):
    .

- lastX (number; optional):
    .

- lastY (number; optional):
    .

- position (dict; optional):
    ."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, onStop=Component.UNDEFINED, axis=Component.UNDEFINED, handle=Component.UNDEFINED, defaultPosition=Component.UNDEFINED, position=Component.UNDEFINED, grid=Component.UNDEFINED, lastX=Component.UNDEFINED, lastY=Component.UNDEFINED, deltaX=Component.UNDEFINED, deltaY=Component.UNDEFINED, ismoved=Component.UNDEFINED, disabled=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'axis', 'defaultPosition', 'deltaX', 'deltaY', 'disabled', 'grid', 'handle', 'ismoved', 'lastX', 'lastY', 'position']
        self._type = 'DragDash'
        self._namespace = 'drag_dash'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'axis', 'defaultPosition', 'deltaX', 'deltaY', 'disabled', 'grid', 'handle', 'ismoved', 'lastX', 'lastY', 'position']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DragDash, self).__init__(children=children, **args)
