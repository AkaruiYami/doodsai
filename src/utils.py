'''
    src/utils.py
'''

def normalize(num:float, val_min:float, val_max:float) -> float:
    '''Given a number, min and max value, returns a float translated to range
    between 0.0 and 1.0.
    @num: float - value between val_min and val_max.
    @val_min: float - min value num can be
    @val_max: float - max value num can be'''
    if not (val_min < num < val_max):
        raise ValueError("num must be a value between val_min and val_max")
    return 0 + (float(num - val_min) / float(val_max - val_min) * (1 - 0))

def standardize(num:float, val_min:float, val_max:float) -> float:
    '''Given a number, min, and max value, returns a float translated to range
    between -1.0 and 1.0.
    @num: float - value between val_min and val_max
    @val_min: float - min value num can be
    @val_max: float - max value num can be'''
    if not (val_min < num < val_max):
        raise ValueError("num must be a value between val_min and val_max")
    return -1 + (float(num - val_min) / float(val_max - val_min) * (1
                  - -1))