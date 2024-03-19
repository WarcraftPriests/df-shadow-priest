"""
builds weapon strings
python build_weapons.py
"""

enchant = "enchant=wafting_devotion_3"

one_hands = {
    # "1h_Torch_of_Primal_Awakening_525": "main_hand=torch_of_primal_awakening,id=200642,ilevel=525,crafted_stats=49/36",  # noqa: E501
    "1h_Vakash_the_Shadowed_Inferno_525": "main_hand=ph_fyrakk_cantrip_1h_mace_int,id=207788,ilevel=525",
    # "1h_Sickle_of_the_White_Stag_528": ""
}

off_hands = {
    "OH_Tricksters_Captivating_Chime_525": "off_hand=tricksters_captivating_chime,id=207796,ilevel=525",  # noqa: E501
    "OH_Crackling_Codex_of_the_Isles_525": "off_hand=crackling_codex_of_the_isles,id=194879,ilevel=525,crafted_stats=49/36"  # noqa: E501
}

combos = [(mh, oh) for mh in one_hands.keys() for oh in off_hands.keys()]

for combo in combos:
    name = combo[0] + "-" + combo[1]
    mh = one_hands[combo[0]] + f",{enchant}"
    oh = off_hands[combo[1]]
    profileset = f"profileset.\"{name}\"+={mh}\nprofileset.\"{name}\"+={oh}\n"
    print(profileset)
