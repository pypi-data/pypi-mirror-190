# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class HeatmapLayer(Component):
    """A HeatmapLayer component.


Keyword arguments:

- blur (number; optional)

- fitBoundsOnLoad (boolean; default True)

- fitBoundsOnUpdate (boolean; default False)

- gradient (dict; optional)

- max (number; optional)

- maxZoom (number; optional)

- minOpacity (number; optional)

- points (list; required)

- radius (number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dl_test'
    _type = 'HeatmapLayer'
    @_explicitize_args
    def __init__(self, points=Component.REQUIRED, longitudeExtractor=Component.UNDEFINED, latitudeExtractor=Component.UNDEFINED, intensityExtractor=Component.UNDEFINED, fitBoundsOnLoad=Component.UNDEFINED, fitBoundsOnUpdate=Component.UNDEFINED, onStatsUpdate=Component.UNDEFINED, max=Component.UNDEFINED, radius=Component.UNDEFINED, maxZoom=Component.UNDEFINED, minOpacity=Component.UNDEFINED, blur=Component.UNDEFINED, gradient=Component.UNDEFINED, **kwargs):
        self._prop_names = ['blur', 'fitBoundsOnLoad', 'fitBoundsOnUpdate', 'gradient', 'max', 'maxZoom', 'minOpacity', 'points', 'radius']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['blur', 'fitBoundsOnLoad', 'fitBoundsOnUpdate', 'gradient', 'max', 'maxZoom', 'minOpacity', 'points', 'radius']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['points']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(HeatmapLayer, self).__init__(**args)
