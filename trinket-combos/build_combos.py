"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations
# pylint: disable=line-too-long

combos = {
    # s2 dungeons (441/447)
    # "Idol_of_Pure_Decay_441": "idol_of_pure_decay,id=193660,ilevel=441",
    "Idol_of_Pure_Decay_447": "idol_of_pure_decay,id=193660,ilevel=447",
    # "Irideus_Fragment_441": "irideus_fragment,id=193743,ilevel=441",
    "Irideus_Fragment_447": "irideus_fragment,id=193743,ilevel=447",
    # "Erupting_Spear_Fragment_441": "erupting_spear_fragment,id=193769,ilevel=441",
    "Erupting_Spear_Fragment_447": "erupting_spear_fragment,id=193769,ilevel=447",
    "Spoils_of_Neltharus_441": "spoils_of_neltharus,id=193773,ilevel=441",
    "Spoils_of_Neltharus_447": "spoils_of_neltharus,id=193773,ilevel=447",
    # "Time_Breaching_Talon_441": "time_breaching_talon,id=193791,ilevel=441", # underperformed
    "Time_Breaching_Talon_447": "time_breaching_talon,id=193791,ilevel=447",
    # "Naraxas_Spiked_Tongue_441": "naraxas_spiked_tongue,id=137349,ilevel=441", # underperformed
    # "Naraxas_Spiked_Tongue_447": "naraxas_spiked_tongue,id=137349,ilevel=447", # underperformed
    # "Rotcrusted_Voodoo_Doll_441": "rotcrusted_voodoo_doll,id=159624,ilevel=441",
    "Rotcrusted_Voodoo_Doll_447": "rotcrusted_voodoo_doll,id=159624,ilevel=447",
    # aberrus the shadowed crucible
    "Screaming_Black_Dragonscale_441": "screaming_black_dragonscale,id=202612,ilevel=441",
    "Screaming_Black_Dragonscale_447": "screaming_black_dragonscale,id=202612,ilevel=447",
    # "Vessel_of_Searing_Shadow_437": "vessel_of_searing_shadow,id=202615,ilevel=437", # underperformed
    "Vessel_of_Searing_Shadow_441": "vessel_of_searing_shadow,id=202615,ilevel=441",
    "Ominous_Chromatic_Essence_Obsidian_441": "ominous_chromatic_essence,id=203729,ilevel=441",
    "Ominous_Chromatic_Essence_Obsidian_444": "ominous_chromatic_essence,id=203729,ilevel=444",
    "Ominous_Chromatic_Essence_Ruby_441": "ominous_chromatic_essence,id=203729,ilevel=441",
    "Ominous_Chromatic_Essence_Ruby_444": "ominous_chromatic_essence,id=203729,ilevel=444",
    "Ominous_Chromatic_Essence_Bronze_441": "ominous_chromatic_essence,id=203729,ilevel=441",
    "Ominous_Chromatic_Essence_Bronze_444": "ominous_chromatic_essence,id=203729,ilevel=444",
    "Ominous_Chromatic_Essence_Azure_441": "ominous_chromatic_essence,id=203729,ilevel=441",
    "Ominous_Chromatic_Essence_Azure_444": "ominous_chromatic_essence,id=203729,ilevel=444",
    "Ominous_Chromatic_Essence_Emerald_441": "ominous_chromatic_essence,id=203729,ilevel=441",
    "Ominous_Chromatic_Essence_Emerald_444": "ominous_chromatic_essence,id=203729,ilevel=444",
    # "Igneous_Flowstone_437": "igneous_flowstone,id=203996,ilevel=437", # NYI?
    "Igneous_Flowstone_447": "igneous_flowstone,id=203996,ilevel=447",  # NYI?
    "Neltharions_Call_to_Suffering_444": "neltharions_call_to_suffering,id=204211,ilevel=444",
    "Neltharions_Call_to_Suffering_457": "neltharions_call_to_suffering,id=204211,ilevel=457",
    # "Beacon_to_the_Beyond_437": "beacon_to_the_beyond,id=203963,ilevel=437", # underperformed
    "Beacon_to_the_Beyond_450": "beacon_to_the_beyond,id=203963,ilevel=450",
    # s1 dungeons (415/421)
    "Voidmenders_Shadowgem_421": "voidmenders_shadowgem,id=110007,ilevel=421",
    "Furious_Ragefeather_421": "furious_ragefeather,id=193677,ilevel=421",
    # vault of the incarnates
    "Whispering_Incarnate_Icon_0_421": "whispering_incarnate_icon,id=194301,ilevel=421",
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
                result += f"profileset.\"{profileset_name}\"+=dragonflight.whispering_incarnate_icon_roles={roles}\n"
            if "Ominous_Chromatic_Essence" in trinket:
                dragonflight = trinket.split("_")[3].lower()
                result += f"profileset.\"{profileset_name}\"+=dragonflight.ominous_chromatic_essence_dragonflight={dragonflight}\n"
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
