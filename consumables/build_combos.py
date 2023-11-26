"""
builds combos of food and weapon runes
python build_combos.py
"""

food = {
    "Fated_Fortune_Cookie": "food=fated_fortune_cookie",
    "Aromatic_Seafood_Platter": "food=aromatic_seafood_platter",
    "Feisty_Fish_Sticks": "food=feisty_fish_sticks",
    "Great_Cerulean_Sea": "food=great_cerulean_sea",
    "Revenge_Served_Cold": "food=revenge_served_cold",
    "Thousandbone_Tongueslicer": "food=thousandbone_tongueslicer",
    "Sizzling_Seafood_Medley": "food=sizzling_seafood_medley",
}

runes = {
    "Temp_Weapon_Howling_Rune_3": "temporary_enchant=main_hand:howling_rune_3",
    "Temp_Weapon_Buzzing_Rune_3": "temporary_enchant=main_hand:buzzing_rune_3",
    "Temp_Weapon_Hissing_Rune_3": "temporary_enchant=main_hand:hissing_rune_3",
}

combos = [(f, r) for f in food.keys() for r in runes.keys()]

for combo in combos:
    name = combo[0] + "-" + combo[1]
    f = food[combo[0]]
    r = runes[combo[1]]
    profileset = f"profileset.\"{name}\"+={f}\nprofileset.\"{name}\"+={r}\n"
    print(profileset)