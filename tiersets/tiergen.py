"""Generates tier.simc tier set combos from base.simc profile"""
import itertools

base_file = 'base.simc'
output_file = 'tier.simc'

def get_item_list(name, combo):
    if len(combo) > 1:
        name = name + combo[0] + "-"
        return get_item_list(name, combo[1:])
    else:
        name = name + combo[0]
        return name

tier = {
    'head': 'head=crest_of_lunar_communion,id=207281',
    'shoulders': 'shoulder=shoulderguardians_of_lunar_communion,id=207279',
    'chest': 'chest=cassock_of_lunar_communion,id=207284,enchant_id=6625',
    'hands': 'hands=touch_of_lunar_communion,id=207282',
    'legs': 'legs=leggings_of_lunar_communion,id=207280,enchant_id=6541'
}

# Normal: 463/476
# Heroic: 483
# Mythic: 489
item_levels = [463, 476, 483, 489]
profiles = []
two_set_combos = list(itertools.combinations(tier.keys(), 2))
four_set_combos = list(itertools.combinations(tier.keys(), 4))
combos = two_set_combos + four_set_combos

for ilevel in item_levels:
    for combo in combos:
        item_list = get_item_list("", combo)
        name = f"{len(combo)}_{item_list}_{ilevel}"
        profile_string = ""
        for item in combo:
            profile_string += f"profileset.\"{name}\"+={tier[item]},ilevel={ilevel}\n"
        profiles.append(profile_string + '\n')

base_file_contents = ""
with open(base_file, 'r') as file:
    base_file_contents = file.readlines()
    base_file_contents.append('\n\n')
    file.close()

with open(output_file, 'w') as file:
    file.writelines(base_file_contents)
    file.writelines(profiles)
    file.close()