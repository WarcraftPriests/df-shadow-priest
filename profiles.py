"""Generates profiles used to sim based on the base profiles"""
import os
from itertools import combinations_with_replacement
import re
import yaml
from internal import utils
from internal.weights import find_weights

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


fightExpressions = {
    "pw": 'fight_style="Patchwerk"',
    "lm": 'fight_style="LightMovement"',
    "hm": 'fight_style="HeavyMovement"',
    "ba": "raid_events+=/adds,count=1,first=30,cooldown=60,duration=20",
    "sa": "raid_events+=/adds,count=3,first=45,cooldown=45,duration=10,distance=5",
    "1": "desired_targets=1",
    "2": "desired_targets=2",
    "3": "enemy=Fluffy_Pillow\nenemy=enemy2\nenemy=enemy3\nraid_events+=/move_enemy,enemy_name=enemy3,cooldown=2000,duration=1000,x=-27,y=-27",  # noqa: E501
    "4": "desired_targets=4",
    "dungeons": 'fight_style="DungeonSlice"',
    "ptr": "ptr=1\n",
    "weights": 'calculate_scale_factors="1"\nscale_only="intellect,crit,mastery,vers,haste"',  # noqa: E501
}


def assure_path_exists(path):
    """Make sure the path exists and contains a folder"""
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def clear_out_folders(path):
    """Clear out any existing files in the given path"""
    assure_path_exists(path)
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except OSError as error:
            print(error)


def build_settings(profile_name_string, weights, dungeons):
    """Add any and all expressions to the bottom of the profile"""
    settings_string = "\n"
    for expression in fightExpressions.items():
        abbreviation = expression[0]
        if abbreviation in profile_name_string:
            settings_string += fightExpressions[abbreviation] + "\n"
    if weights:
        settings_string += fightExpressions["weights"]
    if dungeons:
        season = config["dungeonSeason"]
        if "standard" in profile_name_string:
            r_file_location = (
                f"internal/routes/season{season}/standard/{profile_name_string}.simc"  # noqa: E501
            )
        elif "push" in profile_name_string:
            r_file_location = (
                f"internal/routes/season{season}/push/{profile_name_string}.simc"  # noqa: E501
            )
        else:
            print(f"Profile name is non-standard: {profile_name_string}")
            exit(1)
        with open(r_file_location, "r", encoding="utf8") as r_file:
            data = r_file.read()
            r_file.close()
        settings_string += "\n" + data
    return settings_string


def generate_combination_name(stat_distribution):
    """generates a profile name based on the counts of each stat"""
    mastery = stat_distribution.count("mastery")
    versatility = stat_distribution.count("versatility")
    haste = stat_distribution.count("haste")
    crit = stat_distribution.count("crit")
    return f"M{mastery}_V{versatility}_H{haste}_C{crit}"


def generate_stat_string(stat_distribution, name):
    """generates the gear rating string based on the count of the stat"""
    count = stat_distribution.count(name)
    stats_base = config["stats"]["base"] / 4
    extra_line = "\n" if name == "versatility" else ""
    stat_amount = (count * config["stats"]["steps"]) + int(stats_base)
    return f"gear_{name}_rating={stat_amount}{extra_line}"


def build_stats_files():
    """Build generated.simc stats file from stats.simc"""
    sim_file = "stats.simc"
    base_file = f"{args.dir}{sim_file}"
    stats = config["stats"]["include"]
    stats_base = config["stats"]["base"] / 4
    num_of_steps = (config["stats"]["total"] - config["stats"]["base"]) / config[
        "stats"
    ]["steps"]
    distributions = combinations_with_replacement(stats, int(num_of_steps))
    rating_combinations = []
    for dist in distributions:
        combination = {
            "name": generate_combination_name(dist),
            "mastery": generate_stat_string(dist, "mastery"),
            "versatility": generate_stat_string(dist, "versatility"),
            "haste": generate_stat_string(dist, "haste"),
            "crit": generate_stat_string(dist, "crit"),
        }
        haste = int(combination.get("haste").split("=")[1])
        mastery = int(combination.get("mastery").split("=")[1])
        vers = int(combination.get("versatility").split("=")[1])
        crit = int(combination.get("crit").split("=")[1])
        # remove profiles with too low haste/mastery
        if haste < config["stats"]["min"]["haste"]:
            continue
        if mastery < config["stats"]["min"]["mastery"]:
            continue
        if vers < config["stats"]["min"]["vers"]:
            continue
        if crit < config["stats"]["min"]["crit"]:
            continue
        rating_combinations.append(combination)
    print(f"Simming {len(rating_combinations)} number of combinations")
    output_file = f"{args.dir}/generated.simc"
    base_stats = f"""gear_crit_rating={int(stats_base)}
gear_haste_rating={int(stats_base)}
gear_mastery_rating={int(stats_base)}
gear_versatility_rating={int(stats_base)}\n\n"""
    with open(base_file, "r", encoding="utf8") as b_file:
        data = b_file.read()
        b_file.close()
    with open(output_file, "w+", encoding="utf8") as o_file:
        o_file.writelines(data)
        o_file.writelines(base_stats)
        for combo in rating_combinations:
            for stat in stats:
                o_file.write(f'profileset."{combo.get("name")}"+={combo.get(stat)}\n')


def build_simc_file(talent_string, profile_name):
    """Returns output file name based on talent strings"""
    if talent_string:
        return f"profiles/{talent_string}/{profile_name}.simc"
    return f"profiles/{profile_name}.simc"


def replace_talents(talent_string, data):
    """Replaces the talents variable with the talent string given"""
    if "talents=" in data:
        data = re.sub(r"talents=.*", f"talents={talent_string}", data)
    else:
        data.replace("spec=shadow", f"spec=shadow\ntalents={talent_string}")
    return data


def replace_gear(data, talent_string):
    """replaces gear based on the default in config"""
    # replace gear
    if talent_string is None:
        gear_setup = "default"
    else:
        gear_setup = config["builds"][talent_string]["gearSetup"]
    # special-gear should use nonCantrip set
    if args.dir[:-1] == "special-gear":
        gear_setup = "noCantrip"
    for slot in config["gear"][gear_setup]:
        if slot == "off_hand":
            if config["gear"][gear_setup][slot] != "":
                replacement_string = "off_hand=" + config["gear"][gear_setup][slot]
            else:
                replacement_string = ""
            data = data.replace(f"${{gear.{slot}}}", replacement_string)
        else:
            data = data.replace(f"${{gear.{slot}}}", config["gear"][gear_setup][slot])
    # replace gems
    for gem in config["gems"]:
        data = data.replace(f"${{gems.{gem}}}", config["gems"][gem])
    # replace enchants
    for enchant in config["enchants"]:
        data = data.replace(f"${{enchants.{enchant}}}", config["enchants"][enchant])
    return data


def create_talent_builds():
    """creates profiles from talents.yml"""
    profiles = ""
    with open("internal/talents.yml", "r", encoding="utf8") as talent_file:
        talent_builds = yaml.load(talent_file, Loader=yaml.FullLoader)
        talent_file.close()
    for build in talent_builds["builds"]:
        talent_name = build
        talent_string = talent_builds["builds"][build]
        profiles = profiles + f'profileset."{talent_name}"+=talents={talent_string}\n'
    for build in talent_builds["generated"]:
        talent_name = build
        talent_string = talent_builds["generated"][build]
        profiles = profiles + f'profileset."{talent_name}"+=talents={talent_string}\n'
    return profiles


def get_sim_files(sim_dir):
    # talents use generated files in the builds/ dir
    if sim_dir == "talents":
        return os.listdir("talents/builds/")
    else:
        return config["sims"][sim_dir]["files"]


def build_profiles(talent_string, apl_string):
    """build combination list e.g. pw_sa_1"""
    fight_styles = ["pw", "lm", "hm"]
    add_types = ["sa", "ba", "na"]
    targets = ["1", "2", "3", "4"]
    overrides = ""
    with open("internal/overrides.simc", "r", encoding="utf8") as overrides_file:
        overrides = overrides_file.read()
        overrides_file.close()
    combinations = [
        f"{fight}_{add}_{tar}"
        for fight in fight_styles
        for add in add_types
        for tar in targets  # noqa: E501
    ]
    sim_files = get_sim_files(args.dir[:-1])

    for sim_file in sim_files:
        full_sim_file = ""
        if args.dir[:-1] == "talents":
            full_sim_file += "builds/"
        full_sim_file += sim_file
        with open(f"{args.dir}{full_sim_file}", "r", encoding="utf8") as contents:
            data = contents.read()
            contents.close()
        if args.dungeons:
            combinations = utils.get_dungeon_combos()
        if talent_string:
            if args.dungeons:
                talents_expr = config["builds"][talent_string]["talents"]["dungeons"]
            else:
                talents_expr = config["builds"][talent_string]["talents"]["composite"]
        else:
            talents_expr = ""
        data = replace_gear(data, talent_string)
        # apl override
        data = data.replace("${apl}", apl_string)
        # builds override
        data = data.replace("${builds}", create_talent_builds())
        # insert talents in here so copy= works correctly
        if talents_expr:
            data = data.replace("${talents}", str(talents_expr))

        for profile in combinations:
            # Don't build the profile if it has no weight
            weight = find_weights(config["compositeWeights"]).get(profile) or 0
            st_weight = find_weights(config["singleTargetWeights"]).get(profile) or 0
            two_target_weight = (
                find_weights(config["twoTargetWeights"]).get(profile) or 0
            )
            three_target_weight = (
                find_weights(config["threeTargetWeights"]).get(profile) or 0
            )
            four_target_weight = (
                find_weights(config["fourTargetWeights"]).get(profile) or 0
            )
            if (
                weight == 0
                and st_weight == 0
                and two_target_weight == 0
                and three_target_weight == 0
                and four_target_weight == 0
                and not args.dungeons
            ):  # noqa: E501
                # print(f"Skipping profile {profile} weights are all 0.")
                continue

            sim_data = data
            # prefix the profile name with the base file name
            profile_name = f"{sim_file[:-5]}_{profile}"
            settings = build_settings(
                profile, config["sims"][args.dir[:-1]]["weights"], args.dungeons
            )

            # insert talents based on profile
            if talents_expr:
                if args.dungeons:
                    target_count = 0
                else:
                    target_count = int(profile[-1])
                if profile in config["singleTargetProfiles"]:
                    new_talents = config["builds"][talent_string]["talents"]["single"]
                    sim_data = replace_talents(new_talents, sim_data)
                elif target_count == 2:
                    new_talents = config["builds"][talent_string]["talents"]["2t"]
                    sim_data = replace_talents(new_talents, sim_data)
                elif target_count == 3:
                    new_talents = config["builds"][talent_string]["talents"]["3t"]
                    sim_data = replace_talents(new_talents, sim_data)
                elif target_count == 4:
                    new_talents = config["builds"][talent_string]["talents"]["4t"]
                    sim_data = replace_talents(new_talents, sim_data)
                else:
                    sim_data = replace_talents(talents_expr, sim_data)

            simc_file = build_simc_file(talent_string, profile_name)
            with open(args.dir + simc_file, "w+", encoding="utf8") as o_file:
                if args.ptr:
                    o_file.writelines(fightExpressions["ptr"])
                o_file.writelines(sim_data)
                o_file.writelines(settings)
                o_file.writelines(overrides)
                o_file.close()


if __name__ == "__main__":
    parser = utils.generate_parser("Generates sim profiles.")
    args = parser.parse_args()

    talents = utils.get_talents(args)

    APL = "default_actions=1"

    if args.apl:
        with open("internal/apl.simc", "r", encoding="utf8") as file:
            APL = file.read()
            file.close()

    clear_out_folders(f"{args.dir}output/")
    clear_out_folders(f"{args.dir}profiles/")

    if args.dir[:-1] == "stats":
        build_stats_files()

    if talents:
        for talent in talents:
            clear_out_folders(f"{args.dir}output/{talent}/")
            clear_out_folders(f"{args.dir}profiles/{talent}/")
            print(f"Building {talent} profiles...")
            build_profiles(talent, APL)
    else:
        print("Building default profiles...")
        build_profiles(None, APL)
