"""creates combinations of stones"""
from itertools import combinations

stones = {
    'DBS': 204027,  # Desirous Blood Stone
    'FLS': 204002,  # Flame Licked Stone
    'SIS': 204000,  # Storm Infused Stone
    'ETS': 204001,  # Echoing Thunder Stone
    'EFS': 204005,  # Entropic Fel Stone
    'FIS': 204011,  # Freezing Ice Stone
    'HAS': 204018,  # Humming Arcane Stone
    'PPS': 204022,  # Pestilent Plague Stone
    'OPS': 204007,  # Obscure Pastel Stone
    'PTS': 204029  # Prophetic Twilight Stone
}

def combine_name(combo_string):
    """transforms FIS-FIS-HAS to FIS2-HAS1"""
    new_combo = ""
    entries = combo_string.split("-")
    first = entries.count(entries[0])
    second = entries.count(entries[1])
    third = entries.count(entries[2])

    counted_stones = []
    new_combo = entries[0] + str(first) + "-"
    counted_stones.append(entries[0])

    if entries[1] not in counted_stones:
        new_combo += entries[1] + str(second) + "-"
        counted_stones.append(entries[1])

    if entries[2] not in counted_stones:
        new_combo += entries[2] + str(third) + "-"

    new_combo = new_combo[:-1]

    return new_combo


combos = list(combinations(stones, 3))
profilesets = []

for combo in combos:
    RING_COMBO = ""
    SIMC_STRING = "finger2=onyx_annulet,id=203460,enchant_id=6556,ilevel=424,gem_id="
    for stone in combo:
        RING_COMBO = RING_COMBO + stone + "-"
        SIMC_STRING += str(stones[stone]) + "/"
    RING_COMBO = combine_name(RING_COMBO[:-1])
    SIMC_STRING = SIMC_STRING[:-1]

    profilesets.append(
        f"profileset.\"Onyx_Annulet_2_{RING_COMBO}_424\"+={SIMC_STRING}")

for profileset in profilesets:
    print(profileset)
