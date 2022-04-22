"""weight dict definitions"""

weights_sepulcher_of_the_first_ones = {
    'pw_ba_1': 0.009,
    'pw_sa_1': 0.127,
    'pw_na_1': 0.377,
    'lm_ba_1': 0.003,
    'lm_sa_1': 0.048,
    'lm_na_1': 0.138,
    'hm_ba_1': 0.000,
    'hm_sa_1': 0.000,
    'hm_na_1': 0.027,
    'pw_ba_2': 0.027,
    'pw_sa_2': 0.043,
    'pw_na_2': 0.150,
    'lm_ba_2': 0.005,
    'lm_sa_2': 0.000,
    'lm_na_2': 0.036,
    'hm_ba_2': 0.000,
    'hm_sa_2': 0.000,
    'hm_na_2': 0.009,
}

weights_single = {
    'pw_na_1': 0.69514237856,
    'lm_na_1': 0.25460636516,
    'hm_na_1': 0.05025125628,
}


def find_weights(key):
    """return the matching dict"""
    if key == 'weightsSingle':
        return weights_single
    if key == 'weightsSepulcherOfTheFirstOnes':
        return weights_sepulcher_of_the_first_ones
    return None
