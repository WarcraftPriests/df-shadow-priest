"""weight dict definitions"""

weights_vault_of_the_incarnates = {
    'pw_ba_1': 0.050,
    'pw_sa_1': 0.0833,
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

weights_aberrus_the_shadowed_crucible = {
    'pw_ba_1': 0.08333333,
    'pw_sa_1': 0.17777778,
    'pw_na_1': 0.32777778,
    'lm_ba_1': 0.01111111,
    'lm_sa_1': 0.05555556,
    'lm_na_1': 0.16111111,
    'hm_ba_1': 0.00000000,
    'hm_sa_1': 0.00000000,
    'hm_na_1': 0.06111111,
    'pw_ba_2': 0.01666667,
    'pw_sa_2': 0.00000000,
    'pw_na_2': 0.07222222,
    'lm_ba_2': 0.00000000,
    'lm_sa_2': 0.00000000,
    'lm_na_2': 0.02777778,
    'hm_ba_2': 0.00000000,
    'hm_sa_2': 0.00000000,
    'hm_na_2': 0.00555556,
    'pw_ba_4': 0.00000000,
    'pw_sa_4': 0.00000000,
    'pw_na_4': 0.00000000,
    'lm_ba_4': 0.00000000,
    'lm_sa_4': 0.00000000,
    'lm_na_4': 0.00000000,
    'hm_ba_4': 0.00000000,
    'hm_sa_4': 0.00000000,
    'hm_na_4': 0.00000000,
}

weights_single = {
    'pw_na_1': 0.59595959596,
    'lm_na_1': 0.29292929293,
    'hm_na_1': 0.11111111111,
}

weights_two_targets = {
    'pw_ba_2': 0.000,
    'pw_sa_2': 0.000,
    'pw_na_2': 0.800,
    'lm_ba_2': 0.000,
    'lm_sa_2': 0.000,
    'lm_na_2': 0.200,
    'hm_ba_2': 0.000,
    'hm_sa_2': 0.000,
    'hm_na_2': 0.000,
}

weights_four_targets = {
    'pw_ba_4': 0.000,
    'pw_sa_4': 0.000,
    'pw_na_4': 0.800,
    'lm_ba_4': 0.000,
    'lm_sa_4': 0.000,
    'lm_na_4': 0.200,
    'hm_ba_4': 0.000,
    'hm_sa_4': 0.000,
    'hm_na_4': 0.000,
}

weights_season_one = {
    "algethar-fort": 0.0625,
    "algethar-tyran": 0.0625,
    "azure-fort": 0.0625,
    "azure-tyran": 0.0625,
    "cos-fort": 0.0625,
    "cos-tyran": 0.0625,
    "hov-fort": 0.0625,
    "hov-tyran": 0.0625,
    "nokhud-fort": 0.0625,
    "nokhud-tyran": 0.0625,
    "rlp-fort": 0.0625,
    "rlp-tyran": 0.0625,
    "smbg-fort": 0.0625,
    "smbg-tyran": 0.0625,
    "temple-fort": 0.0625,
    "temple-tyran": 0.0625,
}

# bring down overperforming keys to get a better composite
weights_season_two = {
    "bhh-fort": 0.0600,
    "bhh-tyran": 0.0600,
    "freehold-fort": 0.0575,
    "freehold-tyran": 0.0575,
    "hoi-fort": 0.0750,
    "hoi-tyran": 0.0750,
    "neltharus-fort": 0.0575,
    "neltharus-tyran": 0.0575,
    "nelths-fort": 0.0500,
    "nelths-tyran": 0.0500,
    "ulda-fort": 0.0650,
    "ulda-tyran": 0.0650,
    "ur-fort": 0.0675,
    "ur-tyran": 0.0675,
    "vtp-fort": 0.0675,
    "vtp-tyran": 0.0675,
}


def find_weights(key):
    # pylint: disable=too-many-return-statements
    """return the matching dict"""
    if key == 'weightsSingle':
        return weights_single
    if key == 'weightsTwoTargets':
        return weights_two_targets
    if key == 'weightsFourTargets':
        return weights_four_targets
    if key == 'weightsVaultOfTheIncarnates':
        return weights_vault_of_the_incarnates
    if key == 'weightsAberrusTheShadowedCrucible':
        return weights_aberrus_the_shadowed_crucible
    if key == 'weightsSeasonOne':
        return weights_season_one
    if key == 'weightsSeasonTwo':
        return weights_season_two
    return None
