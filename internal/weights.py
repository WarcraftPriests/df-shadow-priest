"""weight dict definitions"""

weights_vault_of_the_incarnates = {
    'pw_ba_1': 0.050,
    'pw_sa_1': 0.125,
    'pw_na_1': 0.250,
    'lm_ba_1': 0.100,
    'lm_sa_1': 0.163,
    'lm_na_1': 0.075,
    'hm_ba_1': 0.013,
    'hm_sa_1': 0.025,
    'hm_na_1': 0.013,
    'pw_ba_2': 0.000,
    'pw_sa_2': 0.000,
    'pw_na_2': 0.038,
    'lm_ba_2': 0.000,
    'lm_sa_2': 0.000,
    'lm_na_2': 0.025,
    'hm_ba_2': 0.000,
    'hm_sa_2': 0.000,
    'hm_na_2': 0.000,
    'pw_ba_4': 0.000,
    'pw_sa_4': 0.000,
    'pw_na_4': 0.088,
    'lm_ba_4': 0.000,
    'lm_sa_4': 0.000,
    'lm_na_4': 0.038,
    'hm_ba_4': 0.000,
    'hm_sa_4': 0.000,
    'hm_na_4': 0.000,
}

weights_single = {
    'pw_na_1': 0.69514237856,
    'lm_na_1': 0.25460636516,
    'hm_na_1': 0.05025125628,
}

weights_two_targets = {
    'pw_ba_2': 0.000,
    'pw_sa_2': 0.000,
    'pw_na_2': 0.600,
    'lm_ba_2': 0.000,
    'lm_sa_2': 0.000,
    'lm_na_2': 0.400,
    'hm_ba_2': 0.000,
    'hm_sa_2': 0.000,
    'hm_na_2': 0.000,
}

weights_four_targets = {
    'pw_ba_4': 0.000,
    'pw_sa_4': 0.000,
    'pw_na_4': 0.700,
    'lm_ba_4': 0.300,
    'lm_sa_4': 0.000,
    'lm_na_4': 0.000,
    'hm_ba_4': 0.000,
    'hm_sa_4': 0.000,
    'hm_na_4': 0.000,
}


def find_weights(key):
    """return the matching dict"""
    if key == 'weightsSingle':
        return weights_single
    if key == 'weightsTwoTargets':
        return weights_two_targets
    if key == 'weightsFourTargets':
        return weights_four_targets
    if key == 'weightsVaultOfTheIncarnates':
        return weights_vault_of_the_incarnates
    return None
