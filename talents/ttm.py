"""Updates profile names from TTM to be more readable"""

if __name__ == '__main__':
    profiles = [
        "DA-Spike.simc",
        "DA-Flay.simc",
        "DA-Spike_DR.simc",
        "DA-Flay_DR.simc",
        "DA-Spike_TS.simc",
        "DA-Flay_TS.simc",
        "DA-Spike_DR_TS.simc",
        "DA-Flay_DR_TS.simc",
        "VF-Spike.simc",
        "VF-Flay.simc",
        "VF-Spike_DR.simc",
        "VF-Flay_DR.simc",
        "VF-Spike_TS.simc",
        "VF-Flay_TS.simc",
        "VF-Spike_DR_TS.simc",
        "VF-Flay_DR_TS.simc",
    ]
    for profile in profiles:
        OUTPUT_FILE = ""
        lines_seen = set()
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
            if 'Solved loadout ' not in line:
                if line not in lines_seen or line.isspace():
                    lines_seen.add(line)
                    OUTPUT_FILE = OUTPUT_FILE + line
                continue
            TALENT = profile[:2]
            line = line.replace('Solved loadout ', TALENT + "_")
            line = line.replace(
                ' 1111', "_" + profile.split('-')[1].split('.simc')[0])

            # Don't add combos that waste points on TS without Yogg
            if "tormented_spirits" in line and "idol_of_yoggsaron" not in line:
                continue
            # Don't add combos that waste points on Shadow Crash without Whispering Shadows  # noqa: E501
            if "shadow_crash" in line and "whispering_shadows" not in line:
                continue
            # Don't add combos that waste points on Inescapable Torment without Y'Shaarj
            if "inescapable_torment" in line and "yshaarj" not in line:
                continue

            # Make sure you are efficiently spending points
            HALF_SELECTED_MID_TALENTS = 0
            for t in ["maddening_touch", "dark_evangelism", "mind_devourer", "phantasmal_pathogen"]:  # noqa: E501
                if t + ":1" in line:
                    HALF_SELECTED_MID_TALENTS = HALF_SELECTED_MID_TALENTS + 1

            if HALF_SELECTED_MID_TALENTS >= 2:
                continue

            HALF_SELECTED_BOT_TALENTS = 0
            for t in ["mastermind", "screams_of_the_void", "insidious_ire"]:
                if t + ":1" in line:
                    HALF_SELECTED_BOT_TALENTS = HALF_SELECTED_BOT_TALENTS + 1

            if HALF_SELECTED_BOT_TALENTS >= 2:
                continue

            # Only use Deathspeaker with Mastermind or Inescapable Torment
            if "deathspeaker" in line and "mastermind" not in line and "inescapable" not in line:  # noqa: E501
                continue

            idols = ["yshaarj", "nzoth", "yogg", "cthun"]
            IDOLS_USED = ""
            IDOLS_COUNT = 0
            for idol in idols:
                if idol in line:
                    IDOLS_COUNT = IDOLS_COUNT + 1
                    if len(IDOLS_USED) > 1:
                        IDOLS_USED += "_"
                    IDOLS_USED += idol
            if len(IDOLS_USED) > 1:
                IDOLS_USED = "_" + IDOLS_USED
            line = line.replace(
                f'profileset."{TALENT}', f'profileset."{TALENT}{IDOLS_USED}')

            # ONLY ALLOW 2 IDOL BUILDS
            if IDOLS_COUNT > 1 and line not in lines_seen:
                lines_seen.add(line)
                OUTPUT_FILE = OUTPUT_FILE + line

        with open(profile, 'w', encoding="utf8") as file:
            file.writelines(OUTPUT_FILE)
            file.close()
