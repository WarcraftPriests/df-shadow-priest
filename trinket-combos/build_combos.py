"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations

combos = {
    # s4 dungeons (500?)
    "Spoils_of_Neltharus_500": "spoils_of_neltharus,id=193773,ilevel=500",
    # "Ruby_Whelp_Shell_500": "ruby_whelp_shell,id=193757,ilevel=500", # TODO: add combos?
    "Tome_of_Unstable_Power_500": "tome_of_unstable_power,id=193628,ilevel=500",
    "Umbrelskuls_Fractured_Heart_500": "umbrelskuls_fractured_heart,id=193639,ilevel=500",
    "Furious_Ragefeather_500": "furious_ragefeather,id=193677,ilevel=500",
    "Irideus_Fragment_500": "irideus_fragment,id=193743,ilevel=500",
    "Idol_of_Pure_Decay_500": "idol_of_pure_decay,id=193660,ilevel=500",
    "Erupting_Spear_Fragment_500": "erupting_spear_fragment,id=193769,ilevel=500",
    "Time_Breaching_Talon_500": "time_breaching_talon,id=193791,ilevel=500",
    "Emerald_Coachs_Whistle_500": "emerald_coachs_whistle,id=193718,ilevel=500",
    # vault of the incarnates (500?)
    "Conjured_Chillglobe_500": "conjured_chillglobe,id=194300,ilevel=500",
    "Iceblood_Deathsnare_500": "iceblood_deathsnare,id=194304,ilevel=500",
    "Whispering_Incarnate_Icon_0_500": "whispering_incarnate_icon,id=194301,ilevel=500",
    "Whispering_Incarnate_Icon_1_500": "whispering_incarnate_icon,id=194301,ilevel=500",
    "Whispering_Incarnate_Icon_2_500": "whispering_incarnate_icon,id=194301,ilevel=500",
    "Desperate_Invokers_Codex_500": "desperate_invokers_codex,id=194310,ilevel=500",
    "Spiteful_Storm_500": "spiteful_storm,id=194309,ilevel=500",
    # aberrus the shadowed crucible (500?)
    "Screaming_Black_Dragonscale_500": "screaming_black_dragonscale,id=202612,ilevel=500",
    "Vessel_of_Searing_Shadow_500": "vessel_of_searing_shadow,id=202615,ilevel=500",
    "Ominous_Chromatic_Essence_Bronze_500": "ominous_chromatic_essence,id=203729,ilevel=500",  # noqa: E501
    "Ominous_Chromatic_Essence_Azure_500": "ominous_chromatic_essence,id=203729,ilevel=500",  # noqa: E501
    "Ominous_Chromatic_Essence_Emerald_500": "ominous_chromatic_essence,id=203729,ilevel=500",  # noqa: E501
    "Neltharions_Call_to_Suffering_500": "neltharions_call_to_suffering,id=204211,ilevel=500",  # noqa: E501
    "Igneous_Flowstone_500": "igneous_flowstone,id=203996,ilevel=500",
    "Beacon_to_the_Beyond_500": "beacon_to_the_beyond,id=203963,ilevel=500",
    # amirdrassil: the dream's hope (500?)
    "Pips_Emerald_Friendship_Badge_500": "pips_emerald_friendship_badge,id=207168,ilevel=500", # noqa: E501
    "Nymues_Unraveling_Spindle_500": "nymues_unraveling_spindle,id=208615,ilevel=500",
    "Nymues_Unraveling_Spindle_IMMOBILIZED_500": "nymues_unraveling_spindle,id=208615,ilevel=500", # noqa: E501
    "Belorrelos_the_Suncaller_500": "belorrelos_the_suncaller,id=207172,ilevel=500",
    "Augury_of_the_Primal_Flame_500": "augury_of_the_primal_flame,id=208614,ilevel=500",
    "Ashes_of_the_Embersoul_500": "ashes_of_the_embersoul,id=207167,ilevel=500"
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
            if "IMMOBILIZED" in trinket:
                result += f"profileset.\"{profileset_name}\"+=dragonflight.nymue_forced_immobilized=1\n" # noqa: E501
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
