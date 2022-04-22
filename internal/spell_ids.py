"""spell ids to be used in json result files"""
racials = {
    "Human": 20598,
    "Blood_Elf": 28730,
    "Vulpera": 312411,
    "Maghar_Orc": 274738,
    "Undead": 5227,
    "Void_Elf": 255669,
    "Dark_Iron_Dwarf": 265221,
    "Troll": 26297,
    "Lightforged_Draenei": 255647,
    "Orc": 33697,
    "Kul_Tiran": 291628,
    "Goblin": 69042,
    "Draenei": 6562,
    "Panda_Feast": 107072,
    "Panda_Haste": 107072,
    "Panda_Crit": 107072,
    "Panda_Mastery": 107072,
    "Panda_Vers": 107072,
    "Mechagnome": 312923,
    "Nightborne": 255665,
    "Night_Elf_Crit": 154748,
    "Night_Elf_Haste": 154748,
    "Dwarf": 59224,
    "Tauren": 154743,
    "Gnome": 92680,
    "Worgen": 68975,
    "Zandalari_Troll_Kimbul": 292363,
    "Zandalari_Troll_Paku": 292361,
    "Zandalari_Troll_Bwonsamdi": 292360
}

enchants = {
    "Weapon_Lightless_Force": 309620,
    "Weapon_Sinful_Revelation": 309623,
    "Weapon_Celestial_Guidance": 309627,
    "Wrists_Illuminated_Soul": 309608,
    "Wrists_Eternal_Intellect": 309609,
    "Chest_Eternal_Bounds": 323761,
    "Chest_Eternal_Stats": 324773,
    "Chest_Eternal_Insight": 342316,
    "Chest_Sacred_Stats": 323762,
    "Ring_Tenet_of_Critical_Strike": 309616,
    "Ring_Tenet_of_Versatility": 309619,
    "Ring_Tenet_of_Haste": 309617,
    "Ring_Tenet_of_Mastery": 309618,
    "Ring_Bargain_of_Critical_Strike": 309612,
    "Ring_Bargain_of_Versatility": 309615,
    "Ring_Bargain_of_Haste": 309613,
    "Ring_Bargain_of_Mastery": 309614
}

consumables = {
    "Veiled_Augment_Rune": 181468,
    "16_Versatility": 173129,
    "16_Critical_Strike": 173127,
    "16_Mastery": 173130,
    "16_Haste": 173128,
    "Spectral_Flask_of_Power": 171276,
    "Potion_of_Phantom_Fire": 171349,
    "Potion_of_Phantom_Fire_Shadowcore_Oil": 171349,
    "Potion_of_Empowered_Exorcisms": 171352,
    "Potion_of_Empowered_Exorcisms_Shadowcore_Oil": 171352,
    "Potion_of_Spectral_Intellect": 171273,
    "Potion_of_Deathly_Fixation": 171351,
    "Potion_of_Deathly_Fixation_Shadowcore_Oil": 171351,
    "Feast_of_Gluttonous_Hedonism": 172043,
    "Spinefin_Souffle_and_Fries": 172041,
    "Tenebrous_Crown_Roast_Aspic": 172045,
    "Iridescent_Ravioli_with_Apple_Sauce": 172049,
    "Steak_a_la_Mode": 172051,
    "Shadowcore_Oil": 171285,
    "7_Intellect": 168638,
    "6_Intellect": 153709
}

tiersets = {
    "T28-2-set": 364424,
    "T28-2_4-set": 363469
}


def find_ids(key):
    # pylint: disable=too-many-return-statements
    """return the matching dict"""
    if key == 'racials':
        return racials
    if key == 'enchants':
        return enchants
    if key == 'consumables':
        return consumables
    if key == 'tiersets':
        return tiersets
    return None
