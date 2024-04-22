"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations

combos = {
    # s4 dungeons (528)
    "Spoils_of_Neltharus_528": "spoils_of_neltharus,id=193773,ilevel=528",
    # "Ruby_Whelp_Shell_528": "ruby_whelp_shell,id=193757,ilevel=528",
    "Tome_of_Unstable_Power_528": "tome_of_unstable_power,id=212685,ilevel=528",
    "Umbrelskuls_Fractured_Heart_528": "umbrelskuls_fractured_heart,id=212684,ilevel=528",
    "Furious_Ragefeather_528": "furious_ragefeather,id=193677,ilevel=528",
    "Irideus_Fragment_528": "irideus_fragment,id=193743,ilevel=528",
    # "Idol_of_Pure_Decay_528": "idol_of_pure_decay,id=193660,ilevel=528",
    "Erupting_Spear_Fragment_528": "erupting_spear_fragment,id=193769,ilevel=528",
    # "Time_Breaching_Talon_528": "time_breaching_talon,id=193791,ilevel=528",
    # "Emerald_Coachs_Whistle_528": "emerald_coachs_whistle,id=193718,ilevel=528",
    # vault of the incarnates (528)
    # "Conjured_Chillglobe_528": "conjured_chillglobe,id=194300,ilevel=528",
    "Iceblood_Deathsnare_528": "iceblood_deathsnare,id=194304,ilevel=528",
    "Whispering_Incarnate_Icon_DPS_528": "whispering_incarnate_icon,id=194301,ilevel=528",
    "Whispering_Incarnate_Icon_TankDPS_528": "whispering_incarnate_icon,id=194301,ilevel=528",
    "Whispering_Incarnate_Icon_HealerDPS_528": "whispering_incarnate_icon,id=194301,ilevel=528",
    "Whispering_Incarnate_Icon_FULL_528": "whispering_incarnate_icon,id=194301,ilevel=528",
    "Desperate_Invokers_Codex_528": "desperate_invokers_codex,id=194310,ilevel=528",
    # "Spiteful_Storm_528": "spiteful_storm,id=194309,ilevel=528",
    # aberrus the shadowed crucible (528)
    "Screaming_Black_Dragonscale_528": "screaming_black_dragonscale,id=202612,ilevel=528",
    "Vessel_of_Searing_Shadow_528": "vessel_of_searing_shadow,id=202615,ilevel=528",
    "Ominous_Chromatic_Essence_Bronze_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Azure_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Emerald_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Obsidian_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Ruby_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Bronze_AllAllies_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Azure_AllAllies_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Emerald_AllAllies_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Obsidian_AllAllies_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Ominous_Chromatic_Essence_Ruby_AllAllies_528": "ominous_chromatic_essence,id=203729,ilevel=528",
    "Neltharions_Call_to_Suffering_535": "neltharions_call_to_suffering,id=204211,ilevel=535",  # noqa: E501
    "Igneous_Flowstone_528": "igneous_flowstone,id=203996,ilevel=528",
    # "Beacon_to_the_Beyond_528": "beacon_to_the_beyond,id=203963,ilevel=528",
    # amirdrassil: the dream's hope (528)
    "Pips_Emerald_Friendship_Badge_528": "pips_emerald_friendship_badge,id=207168,ilevel=528", # noqa: E501
    "Nymues_Unraveling_Spindle_528": "nymues_unraveling_spindle,id=208615,ilevel=528",
    "Nymues_Unraveling_Spindle_IMMOBILIZED_528": "nymues_unraveling_spindle,id=208615,ilevel=528", # noqa: E501
    "Belorrelos_the_Suncaller_528": "belorrelos_the_suncaller,id=207172,ilevel=528",
    "Augury_of_the_Primal_Flame_535": "augury_of_the_primal_flame,id=208614,ilevel=535",
    "Ashes_of_the_Embersoul_528": "ashes_of_the_embersoul,id=207167,ilevel=528"
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
                allies = trinket.split("_")[3].lower()
                roles = ""
                if allies == "dps":
                    roles = "dps"
                elif allies == "tankdps":
                    roles = "dps/tank"
                elif allies == "healerdps":
                    roles = "dps/heal"
                elif allies == "full":
                    roles = "tank/heal/dps"
                else:
                    exit("No allies found")
                result += f"profileset.\"{profileset_name}\"+=dragonflight.whispering_incarnate_icon_roles={roles}\n"  # noqa: E501
            if "Ominous_Chromatic_Essence" in trinket:
                dragonflight = trinket.split("_")[3].lower()
                result += f"profileset.\"{profileset_name}\"+=dragonflight.ominous_chromatic_essence_dragonflight={dragonflight}\n"  # noqa: E501
            if "AllAllies" in trinket:
                result += f"profileset.\"{profileset_name}\"+=dragonflight.ominous_chromatic_essence_allies=azure/bronze/obsidian/ruby\n"  # noqa: E501
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
