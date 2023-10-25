"""
builds weapon strings
python build_weapons.py
"""

enchant = "enchant=sophic_devotion_3"

one_hands = {
    "1h_Wand_of_Zealous_Purification_483": "main_hand=wand_of_zealous_purification,id=158321,ilevel=483",  # noqa: E501
    "1h_Wand_of_Zealous_Purification_489": "main_hand=wand_of_zealous_purification,id=158321,ilevel=489",  # noqa: E501
    "1h_Morchies_Distorted_Spellblade_483": "main_hand=morchies_distorted_spellblade,id=207997,ilevel=483",  # noqa: E501
    "1h_Morchies_Distorted_Spellblade_489": "main_hand=morchies_distorted_spellblade,id=207997,ilevel=489",  # noqa: E501
    "1h_Torch_of_Primal_Awakening_483": "main_hand=torch_of_primal_awakening,id=200642,ilevel=483,crafted_stats=49/36",  # noqa: E501
    "1h_Vakash_the_Shadowed_Inferno_483": "main_hand=ph_fyrakk_cantrip_1h_mace_int,id=207788,ilevel=483",
    "1h_Vakash_the_Shadowed_Inferno_489": "main_hand=ph_fyrakk_cantrip_1h_mace_int,id=207788,ilevel=489",
}

off_hands = {
    "OH_Ancestors_Necromantic_Focus_483": "off_hand=ancestors_necromantic_focus,id=207983,ilevel=483",  # noqa: E501
    "OH_Ancestors_Necromantic_Focus_489": "off_hand=ancestors_necromantic_focus,id=207983,ilevel=489",  # noqa: E501
    "OH_Interlopers_Mossy_Skull_483": "off_hand=interlopers_mossy_skull,id=119176,ilevel=483",  # noqa: E501
    "OH_Interlopers_Mossy_Skull_489": "off_hand=interlopers_mossy_skull,id=119176,ilevel=489",  # noqa: E501
    "OH_Tricksters_Captivating_Chime_483": "off_hand=tricksters_captivating_chime,id=207796,ilevel=483",  # noqa: E501
    "OH_Tricksters_Captivating_Chime_489": "off_hand=tricksters_captivating_chime,id=207796,ilevel=489",  # noqa: E501
    "OH_Crackling_Codex_of_the_Isles_483": "off_hand=crackling_codex_of_the_isles,id=194879,ilevel=483,crafted_stats=49/36"  # noqa: E501
}

combos = [(mh, oh) for mh in one_hands.keys() for oh in off_hands.keys()]

for combo in combos:
    name = combo[0] + "-" + combo[1]
    mh = one_hands[combo[0]] + f",{enchant}"
    oh = off_hands[combo[1]]
    profileset = f"profileset.\"{name}\"+={mh}\nprofileset.\"{name}\"+={oh}\n"
    print(profileset)
