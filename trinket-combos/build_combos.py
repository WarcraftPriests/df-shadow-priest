"""
builds trinket strings
python build_combos.py
"""

from itertools import combinations
# pylint: disable=line-too-long

combos = {
    # dungeons (402/418)
    "Infernal_Wrist_402": "infernal_wrist,id=137485,ilevel=402",
    "Infernal_Wrist_418": "infernal_wrist,id=137485,ilevel=418",
    "Eye_of_Skovald_402": "eye_of_skovald,id=133641,ilevel=402",
    "Eye_of_Skovald_418": "eye_of_skovald,id=133641,ilevel=418",
    "Horn_of_Valor_402": "horn_of_valor,id=133642,ilevel=402",
    "Horn_of_Valor_418": "horn_of_valor,id=133642,ilevel=418",
    # "Voidmenders_Shadowgem_402": "voidmenders_shadowgem,id=110007,ilevel=402",
    # "Voidmenders_Shadowgem_418": "voidmenders_shadowgem,id=110007,ilevel=418",
    # "Blazebinders_Hoof_402": "blazebinders_hoof,id=193762,ilevel=402",
    # "Blazebinders_Hoof_418": "blazebinders_hoof,id=193762,ilevel=418",
    # "Ruby_Whelp_Shell_402": "ruby_whelp_shell,id=193757,ilevel=402",
    # "Ruby_Whelp_Shell_418": "ruby_whelp_shell,id=193757,ilevel=418",
    # "Tome_of_Unstable_Power_402": "tome_of_unstable_power,id=193628,ilevel=402",
    # "Tome_of_Unstable_Power_418": "tome_of_unstable_power,id=193628,ilevel=418",
    # "Umbrelskuls_Fractured_Heart_402": "umbrelskuls_fractured_heart,id=193639,ilevel=402",
    # "Umbrelskuls_Fractured_Heart_418": "umbrelskuls_fractured_heart,id=193639,ilevel=418",
    # "Furious_Ragefeather_402": "furious_ragefeather,id=193677,ilevel=402",
    # "Furious_Ragefeather_418": "furious_ragefeather,id=193677,ilevel=418",
    # vault of the incarnates
    "Conjured_Chillglobe_402": "conjured_chillglobe,id=194300,ilevel=402",
    "Conjured_Chillglobe_415": "conjured_chillglobe,id=194300,ilevel=415",
    # "Iceblood_Deathsnare_402": "iceblood_deathsnare,id=194304,ilevel=402",
    # "Iceblood_Deathsnare_415": "iceblood_deathsnare,id=194304,ilevel=415",
    "Whispering_Incarnate_Icon_0_408": "whispering_incarnate_icon,id=194301,ilevel=408",
    "Whispering_Incarnate_Icon_0_421": "whispering_incarnate_icon,id=194301,ilevel=421",
    "Whispering_Incarnate_Icon_1_408": "whispering_incarnate_icon,id=194301,ilevel=408",
    "Whispering_Incarnate_Icon_1_421": "whispering_incarnate_icon,id=194301,ilevel=421",
    "Whispering_Incarnate_Icon_2_408": "whispering_incarnate_icon,id=194301,ilevel=408",
    "Whispering_Incarnate_Icon_2_421": "whispering_incarnate_icon,id=194301,ilevel=421",
    # "Broodkeepers_Promise_411": "broodkeepers_promise,id=194307,ilevel=411",
    # "Broodkeepers_Promise_424": "broodkeepers_promise,id=194307,ilevel=424",
    # "Desperate_Invokers_Codex_411": "desperate_invokers_codex,id=194310,ilevel=411",
    # "Desperate_Invokers_Codex_424": "desperate_invokers_codex,id=194310,ilevel=424",
    "Spiteful_Storm_411": "spiteful_storm,id=194309,ilevel=411",
    "Spiteful_Storm_424": "spiteful_storm,id=194309,ilevel=424",
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
