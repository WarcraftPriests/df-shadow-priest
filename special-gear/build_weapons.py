"""
builds weapon strings
python build_weapons.py
"""

enchant = "enchant=wafting_devotion_3"

one_hands = {
    "1h_Vakash_the_Shadowed_Inferno_528": "main_hand=vakash_the_shadowed_inferno,id=207788,ilevel=528",
}

off_hands = {
    "OH_Tricksters_Captivating_Chime_528": "off_hand=tricksters_captivating_chime,id=207796,ilevel=528",  # noqa: E501
    "OH_Crackling_Codex_of_the_Isles_525": "off_hand=crackling_codex_of_the_isles,id=194879,ilevel=525,crafted_stats=49/36",  # noqa: E501
    "OH_Echos_Maddening_Volume_528": "off_hand=echos_maddening_volume,id=204324,ilevel=528",
    "OH_Thadrions_Erratic_Arcanotrode_528": "off_hand=thadrions_erratic_arcanotrode,id=204318,ilevel=528",
    "OH_Scripture_of_Primal_Devotion_528": "off_hand=scripture_of_primal_devotion,id=195513,ilevel=528",
    "OH_Icewraths_Channeling_Conduit_528": "off_hand=icewraths_channeling_conduit,id=195484,ilevel=528",
    "OH_Rod_of_Perfect_Order_528": "off_hand=rod_of_perfect_order,id=193745,ilevel=528",
}

combos = [(mh, oh) for mh in one_hands.keys() for oh in off_hands.keys()]

for combo in combos:
    name = combo[0] + "-" + combo[1]
    mh = one_hands[combo[0]] + f",{enchant}"
    oh = off_hands[combo[1]]
    profileset = f"profileset.\"{name}\"+={mh}\nprofileset.\"{name}\"+={oh}\n"
    print(profileset)
