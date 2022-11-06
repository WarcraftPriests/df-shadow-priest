"""spell ids to be used in json result files"""
consumables = {
    "Iced_Phial_of_Corrupting_Rage": 191329,
    "Phial_of_Charged_Isolation": 191332,
    "Phial_of_Elemental_Chaos": 191359,
    "Phial_of_Glacial_Fury": 191335,
    "Phial_of_Static_Empowerment": 191338,
    "Phial_of_Tepid_Versatility": 191341,
    "Bottled_Putrescence": 191362,
    "Elemental_Potion_of_Power": 191389,
    "Elemental_Potion_of_Ultimate_Power": 191383,
    "Potion_of_Shocking_Disclosure": 191401,
    "Draconic_Augment_Rune": 201325,
    "Yusas_Hearty_Stew": 197793,
    "Grand_Banquet_of_the_Kaluak": 197794,
    "Hoard_of_Draconic_Delicacies": 197795,
    "Fated_Fortune_Cookie": 197792,
    "Filet_of_Fangs": 197779,
    "Salt_Baked_Fishcake": 197781,
    "Seamoth_Surprise": 197780,
    "Timely_Demise": 197778,
    "Aromatic_Seafood_Platter": 197783,
    "Feisty_Fish_Sticks": 197782,
    "Great_Cerulean_Sea": 197787,
    "Revenge_Served_Cold": 197785,
    "Thousandbone_Tongueslicer": 197786,
    "Sizzling_Seafood_Medley": 197784,
    "Roast_Duck_Delight": 197790,
    "Thrice_Spiced_Mammoth_Kabob": 197776
}

enchants = {
    "Legs_Frozen_Spellthread": 194013,
    "Legs_Temporal_Spellthread": 194016,
    "Legs_Vibrant_Spellthread": 194010,
    "Weapon_Burning_Writ": 200051,
    "Weapon_Earthen_Writ": 200053,
    "Weapon_Frozen_Writ": 200057,
    "Weapon_Sophic_Writ": 200055,
    "Weapon_Wafting_Writ": 200059,
    "Weapon_Frozen_Devotion": 200056,
    "Weapon_Sophic_Devotion": 200054,
    "Weapon_Wafting_Devotion": 200058,
    "Chest_Reserve_of_Intellect": 200028,
    "Chest_Waking_Stats": 200030,
    "Ring_Devotion_of_Critical_Strike": 200037,
    "Ring_Devotion_of_Haste": 200038,
    "Ring_Devotion_of_Mastery": 200039,
    "Ring_Devotion_of_Versatility": 200040,
    "Ring_Writ_of_Critical_Strike": 200041,
    "Ring_Writ_of_Haste": 200042,
    "Ring_Writ_of_Mastery": 200043,
    "Ring_Writ_of_Versatility": 200044,
}

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
    "Zandalari_Troll_Bwonsamdi": 292360,
    "Highmountain_Tauren": 255658
}

tiersets = {
    "T29-2-set": 394961,
    "T29-2_4-set": 394963
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
