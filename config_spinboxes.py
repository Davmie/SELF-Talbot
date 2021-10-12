spinboxes_to_create_rect = [
    {
        'name': 'b',
        'label': 'Длина выреза',
        'type': float,
        'min_value': 0.1,
        'max_value': 2,
        'step': 0.1,
        'default_value': 0.1,
    },
    {
        'name': 'p',
        'label': 'Период',
        'type': float,
        'min_value': 0.1,
        'max_value': 2,
        'step': 0.1,
        'default_value': 1,
    },
    {
        'name': 'k',
        'label': 'x = [-kx; kx]\nКоэфф у х',
        'type': int,
        'min_value': 1,
        'max_value': 10,
        'step': 1,
        'default_value': 2,
    },
    {
        'name': 'zt',
        'label': 'Zt',
        'type': float,
        'min_value': 0,
        'max_value': 1,
        'step': 0.05,
        'default_value': 0.4,
    },
]

spinboxes_to_create_wave = [
    {
        'name': 'p',
        'label': 'Период',
        'type': float,
        'min_value': 0.1,
        'max_value': 2,
        'step': 0.1,
        'default_value': 1,
    },
    {
        'name': 'k',
        'label': 'x = [-kx; kx]\nКоэфф у х',
        'type': int,
        'min_value': -10,
        'max_value': 10,
        'step': 1,
        'default_value': 2,
    },
    {
        'name': 'zt',
        'label': 'Zt',
        'type': float,
        'min_value': 0,
        'max_value': 1,
        'step': 0.05,
        'default_value': 0.4,
    },
]
