spinboxes_to_create_rect = [
    {
        'name': 'b',
        'label': 'Длина выреза',
        'type': float,
        'min_value': 0.000000001,
        'max_value': 2,
        'step': 0.1,
        'default_value': 0.1,
    },
    {
        'name': 'p',
        'label': 'Период',
        'type': float,
        'min_value': 0.000001,
        'max_value': 10,
        'step': 0.1,
        'default_value': 1,
    },
    {
        'name': 'k',
        'label': 'x = [-kp; kp]   k:',
        'type': float,
        'min_value': 0,
        'max_value': 40,
        'step': 1,
        'default_value': 2,
    },
    {
        'name': 'zt',
        'label': 'z = [0; n*Zt]    n:',
        'type': float,
        'min_value': 0,
        'max_value': 1,
        'step': 0.05,
        'default_value': 0.4,
    },
    {
        'name': 'z0',
        'label': 'm * Zt\t        m:\n(график)',
        'type': float,
        'min_value': 0,
        'max_value': 1,
        'step': 0.05,
        'default_value': 0.2
    },
]

spinboxes_to_create_wave = [
    {
        'name': 'p',
        'label': 'Период',
        'type': float,
        'min_value': 0.005,
        'max_value': 1,
        'step': 0.1,
        'default_value': 5,
    },
    {
        'name': 'k',
        'label': 'x = [-kp; kp]   k:',
        'type': float,
        'min_value': 0,
        'max_value': 40,
        'step': 1,
        'default_value': 2,
    },
    {
        'name': 'zt',
        'label': 'z = [0; n*Zt]    n:',
        'type': float,
        'min_value': 0.01,
        'max_value': 5,
        'step': 0.05,
        'default_value': 1,
    },
    {
        'name': 'z0',
        'label': 'm * Zt\t        m:\n(график)',
        'type': float,
        'min_value': 0,
        'max_value': 1,
        'step': 0.05,
        'default_value': 0.2,
    },
]
