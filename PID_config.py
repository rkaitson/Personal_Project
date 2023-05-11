settings = {
    "name": "PID",
    "num_samples": 1024, # number of trials
    "metric": "val_score", # don't change this
    "minimize": True, # ""
    "mode": "min", # ""
}

params = [
    {
        "name": "Kp",
        "type": "range",
        "bounds": [1E-3,100],
        "log_scale": True,
        "value_type": "float",
    },
    {
        "name": "Ki",
        "type": "range",
        "bounds": [1E-3,100],
        "log_scale": True,
        "value_type": "float",
    },
    {
        "name": "Kd",
        "type": "range",
        "bounds": [1E-3,100],
        "log_scale": True,
        "value_type": "float",
    },
]

config = {'settings': settings, 'params': params}
