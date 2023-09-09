"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations

combos = {
    # s2 dungeons (441/447)
    "Spoils_of_Neltharus_447": "spoils_of_neltharus,id=193773,ilevel=447",
    # aberrus the shadowed crucible
    "Vessel_of_Searing_Shadow_447": "vessel_of_searing_shadow,id=202615,ilevel=447",
    "Ominous_Chromatic_Essence_Bronze_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    "Ominous_Chromatic_Essence_Azure_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    "Ominous_Chromatic_Essence_Emerald_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    "Neltharions_Call_to_Suffering_457": "neltharions_call_to_suffering,id=204211,ilevel=457",  # noqa: E501
    # s3 dungeons (470/483)
    "Vessel_of_Skittering_Shadows_470": "vessel_of_skittering_shadows,id=159610,ilevel=470", # noqa: E501
    "Vessel_of_Skittering_Shadows_483": "vessel_of_skittering_shadows,id=159610,ilevel=483", # noqa: E501
    "Caged_Horror_470": "caged_horror,id=136716,ilevel=470",
    "Caged_Horror_483": "caged_horror,id=136716,ilevel=483",
    "Corrupted_Starlight_470": "corrupted_starlight,id=137301,ilevel=470",
    "Corrupted_Starlight_483": "corrupted_starlight,id=137301,ilevel=483",
    "Oakhearts_Gnarled_Root_470": "oakhearts_gnarled_root,id=137306,ilevel=470",
    "Oakhearts_Gnarled_Root_483": "oakhearts_gnarled_root,id=137306,ilevel=483",
    "Leaf_of_the_Ancient_Protectors_470": "leaf_of_the_ancient_protectors,id=110009,ilevel=470", # noqa: E501
    "Leaf_of_the_Ancient_Protectors_483": "leaf_of_the_ancient_protectors,id=110009,ilevel=483", # noqa: E501
    "Coagulated_Genesaur_Blood_470": "coagulated_genesaur_blood,id=110004,ilevel=470",
    "Coagulated_Genesaur_Blood_483": "coagulated_genesaur_blood,id=110004,ilevel=483",
    "Sea_Star_470": "sea_star,id=133201,ilevel=470",
    "Sea_Star_483": "sea_star,id=133201,ilevel=483",
    "Balefire_Branch_470": "balefire_branch,id=159630,ilevel=470",
    "Balefire_Branch_483": "balefire_branch,id=159630,ilevel=483",
    "Mirror_of_Fractured_Tomorrows_470": "mirror_of_fractured_tomorrows,id=207581,ilevel=470", # noqa: E501
    "Mirror_of_Fractured_Tomorrows_483": "mirror_of_fractured_tomorrows,id=207581,ilevel=483", # noqa: E501
    "Time_Thiefs_Gambit_470": "timethiefs_gambit,id=207579,ilevel=470",
    "Time_Thiefs_Gambit_483": "timethiefs_gambit,id=207579,ilevel=483",
    # amirdrassil: the dream's hope (482/489)
    "Pips_Emerald_Friendship_Badge_Mastery_482": "pips_emerald_friendship_badge_mastery,id=207168,ilevel=482", # noqa: E501
    "Pips_Emerald_Friendship_Badge_Mastery_489": "pips_emerald_friendship_badge_mastery,id=207168,ilevel=489", # noqa: E501
    "Nymues_Vengeful_Spindle_482": "nymues_vengeful_spindle,id=208615,ilevel=482",
    "Nymues_Vengeful_Spindle_489": "nymues_vengeful_spindle,id=208615,ilevel=489",
    "Belorrelos_the_Sunstone_482": "belorrelos_the_sunstone,id=207172,ilevel=482",
    "Belorrelos_the_Sunstone_489": "belorrelos_the_sunstone,id=207172,ilevel=489",
    "Augury_of_the_Primal_Flame_482": "augury_of_the_primal_flame,id=208614,ilevel=482",
    "Augury_of_the_Primal_Flame_489": "augury_of_the_primal_flame,id=208614,ilevel=489",
    "Ashes_of_the_Embersoul_482": "ashes_of_the_embersoul,id=207167,ilevel=482",
    "Ashes_of_the_Embersoul_489": "ashes_of_the_embersoul,id=207167,ilevel=489"
}


def item_id(trinket):
    """given a comma-separated definition for a trinket, returns just the id"""
    i = trinket.split(",")[1]
    return i[3:]


def build_combos():
    """generates the combination list with unique equipped trinkets only"""
    trinkets = combinations(combos.keys(), 2)
    unique_trinkets = []
    for pair in trinkets:
        # check if item id matches, trinkets are unique
        if item_id(combos[pair[0]]) != item_id(combos[pair[1]]):
            unique_trinkets.append(pair)
    print(f"Generated {len(unique_trinkets)} combinations.")
    return unique_trinkets


def build_simc_string(trinkets):
    """build profileset for each trinket combination"""
    result = ""
    for combo in trinkets:
        for trinket in combo:
            trinket_one = combo[0]
            trinket_two = combo[1]
            trinket_one_value = combos[trinket_one]
            trinket_two_value = combos[trinket_two]
            profileset_name = f"{trinket_one}-{trinket_two}"
            if "Whispering_Incarnate_Icon" in trinket:
                allies_count = trinket.split("_")[3].lower()
                roles = ""
                if int(allies_count) == 0:
                    roles = "dps"
                elif int(allies_count) == 1:
                    roles = "dps/tank"
                elif int(allies_count) == 2:
                    roles = "tank/heal/dps"
                result += f"profileset.\"{profileset_name}\"+=dragonflight.whispering_incarnate_icon_roles={roles}\n"  # noqa: E501
            if "Ominous_Chromatic_Essence" in trinket:
                dragonflight = trinket.split("_")[3].lower()
                result += f"profileset.\"{profileset_name}\"+=dragonflight.ominous_chromatic_essence_dragonflight={dragonflight}\n"  # noqa: E501
            if "Pips_Emerald_Friendship_Badge" in trinket:
                stat = trinket.split("_")[4].lower()
                result += f"# profileset.\"{profileset_name}\"+=dragonflight.TODO={stat}\n"  # noqa: E501
        result += f"profileset.\"{profileset_name}\"+=trinket1={trinket_one_value}\n"
        result += f"profileset.\"{profileset_name}\"+=trinket2={trinket_two_value}\n\n"
    return result


def generate_sim_file(input_string):
    """reads in the base simc file and creates the generated.simc file"""
    with open("base.simc", 'r', encoding="utf8") as file:
        data = file.read()
        file.close()
    with open("generated.simc", 'w+', encoding="utf8") as file:
        file.writelines(data)
        file.writelines(input_string)


if __name__ == '__main__':
    trinket_combos = build_combos()
    SIMC_STRING = build_simc_string(trinket_combos)
    generate_sim_file(SIMC_STRING)
