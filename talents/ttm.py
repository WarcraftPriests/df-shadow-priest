"""Updates profile names from TTM to be more readable"""

if __name__ == '__main__':
    profiles = ["VF-ST.simc", "DA-ST.simc", "VF-AoE.simc", "DA-AoE.simc"]
    for profile in profiles:
        OUTPUT_FILE = ""
        with open(profile, 'r', encoding="utf8") as file:
            data = file.readlines()
            file.close()

        SIGNATURE = "# Automatically generated by ttm.py\n"
        if data[0] != SIGNATURE:
            data = [SIGNATURE] + data
        else:
            print(f"{profile} has already been generated, skipping file.")
            continue

        for line in data:
            TALENT = profile[:2]
            line = line.replace('Solved loadout ', TALENT + "_")
            line = line.replace(
                ' 2111122', "_" + profile.split('-')[1].split('.simc')[0])

            idols = ["yshaarj", "cthun", "yogg", "nzoth"]
            IDOLS_USED = ""
            for idol in idols:
                if idol in line:
                    if len(IDOLS_USED) > 1:
                        IDOLS_USED += "_"
                    IDOLS_USED += idol
            if len(IDOLS_USED) > 1:
                IDOLS_USED = "_" + IDOLS_USED
            line = line.replace(
                f'profileset."{TALENT}', f'profileset."{TALENT}{IDOLS_USED}')

            OUTPUT_FILE = OUTPUT_FILE + line

        with open(profile, 'w', encoding="utf8") as file:
            file.writelines(OUTPUT_FILE)
            file.close()
