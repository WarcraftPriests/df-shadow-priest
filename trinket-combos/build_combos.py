"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations

combos = {
    # s2 dungeons (441/447)
    # "Spoils_of_Neltharus_447": "spoils_of_neltharus,id=193773,ilevel=447",
    # aberrus the shadowed crucible
    # "Vessel_of_Searing_Shadow_447": "vessel_of_searing_shadow,id=202615,ilevel=447",
    # "Ominous_Chromatic_Essence_Bronze_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    # "Ominous_Chromatic_Essence_Azure_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    # "Ominous_Chromatic_Essence_Emerald_447": "ominous_chromatic_essence,id=203729,ilevel=447",  # noqa: E501
    # "Neltharions_Call_to_Suffering_457": "neltharions_call_to_suffering,id=204211,ilevel=457",  # noqa: E501
    # timewalking (476)
    "Energy_Siphon_476": "energy_siphon,id=156021,ilevel=476",
    "Living_Flame_476": "living_flame,id=155947,ilevel=476",
    # s3 dungeons (483/489)
    # "Vessel_of_Skittering_Shadows_483": "vessel_of_skittering_shadows,id=159610,ilevel=483", # noqa: E501
    "Vessel_of_Skittering_Shadows_489": "vessel_of_skittering_shadows,id=159610,ilevel=489", # noqa: E501
    # "Caged_Horror_483": "caged_horror,id=136716,ilevel=483",
    "Caged_Horror_489": "caged_horror,id=136716,ilevel=489",
    # "Corrupted_Starlight_483": "corrupted_starlight,id=137301,ilevel=483",
    "Corrupted_Starlight_489": "corrupted_starlight,id=137301,ilevel=489",
    # "Oakhearts_Gnarled_Root_483": "oakhearts_gnarled_root,id=137306,ilevel=483",
    "Oakhearts_Gnarled_Root_489": "oakhearts_gnarled_root,id=137306,ilevel=489",
    # "Coagulated_Genesaur_Blood_483": "coagulated_genesaur_blood,id=110004,ilevel=483",
    "Coagulated_Genesaur_Blood_489": "coagulated_genesaur_blood,id=110004,ilevel=489",
    "Sea_Star_483": "sea_star,id=133201,ilevel=483",
    "Sea_Star_489": "sea_star,id=133201,ilevel=489",
    "Balefire_Branch_483": "balefire_branch,id=159630,ilevel=483",
    "Balefire_Branch_489": "balefire_branch,id=159630,ilevel=489",
    # "Lady_Waycrests_Music_Box_483": "lady_waycrests_music_box,id=159631,ilevel=483", # TODO: BROKEN  # noqa: E501
    "Lady_Waycrests_Music_Box_489": "lady_waycrests_music_box,id=159631,ilevel=489",
    "Mirror_of_Fractured_Tomorrows_483": "mirror_of_fractured_tomorrows,id=207581,ilevel=483", # noqa: E501
    "Mirror_of_Fractured_Tomorrows_489": "mirror_of_fractured_tomorrows,id=207581,ilevel=489", # noqa: E501
    "Time_Thiefs_Gambit_483": "timethiefs_gambit,id=207579,ilevel=483",
    "Time_Thiefs_Gambit_489": "timethiefs_gambit,id=207579,ilevel=489",
    # amirdrassil: the dream's hope (483/489)
    "Pips_Emerald_Friendship_Badge_483": "pips_emerald_friendship_badge,id=207168,ilevel=483", # noqa: E501
    "Pips_Emerald_Friendship_Badge_489": "pips_emerald_friendship_badge,id=207168,ilevel=489", # noqa: E501
    "Nymues_Unraveling_Spindle_483": "nymues_unraveling_spindle,id=208615,ilevel=483",
    "Nymues_Unraveling_Spindle_489": "nymues_unraveling_spindle,id=208615,ilevel=489",
    "Belorrelos_the_Suncaller_483": "belorrelos_the_suncaller,id=207172,ilevel=483",
    "Belorrelos_the_Suncaller_489": "belorrelos_the_suncaller,id=207172,ilevel=489",
    "Augury_of_the_Primal_Flame_483": "augury_of_the_primal_flame,id=208614,ilevel=483",  # noqa: E501
    "Augury_of_the_Primal_Flame_496": "augury_of_the_primal_flame,id=208614,ilevel=496",
    # "Ashes_of_the_Embersoul_483": "ashes_of_the_embersoul,id=207167,ilevel=483",
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
