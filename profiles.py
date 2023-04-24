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
    "ba": 'raid_events+=/adds,count=1,first=30,cooldown=60,duration=20',
    "sa": 'raid_events+=/adds,count=3,first=45,cooldown=45,duration=10,distance=5',
    "1": 'desired_targets=1',
    "2": 'desired_targets=2',
    "4": 'desired_targets=4',
    "dungeons": 'fight_style="DungeonSlice"',
    "ptr": 'ptr=1\n',
    "weights": 'calculate_scale_factors="1"\nscale_only="intellect,crit,mastery,vers,haste"'
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
    settings_string = '\n'
    for expression in fightExpressions.items():
        abbreviation = expression[0]
        if abbreviation in profile_name_string:
            settings_string += fightExpressions[abbreviation] + "\n"
    if weights:
        settings_string += fightExpressions['weights']
    if dungeons:
        season = config["dungeonSeason"]
        r_file_location = f"internal/routes/season{season}/{profile_name_string}.simc"
        with open(r_file_location, 'r', encoding="utf8") as r_file:
            data = r_file.read()
            r_file.close()
        settings_string += "\n" + data
    return settings_string


def generate_combination_name(stat_distribution):
    """generates a profile name based on the counts of each stat"""
    mastery = stat_distribution.count('mastery')
    versatility = stat_distribution.count('versatility')
    haste = stat_distribution.count('haste')
    crit = stat_distribution.count('crit')
    return f"M{mastery}_V{versatility}_H{haste}_C{crit}"


def generate_stat_string(stat_distribution, name):
    """generates the gear rating string based on the count of the stat"""
    count = stat_distribution.count(name)
    stats_base = config["stats"]["base"] / 4
    extra_line = "\n" if name == "versatility" else ""
    stat_amount = (count * config["stats"]["steps"]) + int(stats_base)
    return f"gear_{name}_rating={stat_amount}{extra_line}"


def build_stats_files():
    # pylint: disable=too-many-locals
    """Build generated.simc stats file from stats.simc"""
    sim_file = 'stats.simc'
    base_file = f"{args.dir}{sim_file}"
    stats = config["stats"]["include"]
    stats_base = config["stats"]["base"] / 4
    num_of_steps = (config["stats"]["total"] -
                    config["stats"]["base"]) / config["stats"]["steps"]
    distributions = combinations_with_replacement(stats, int(num_of_steps))
    rating_combinations = []
    for dist in distributions:
        combination = {
            "name": generate_combination_name(dist),
            "mastery": generate_stat_string(dist, "mastery"),
            "versatility": generate_stat_string(dist, "versatility"),
            "haste": generate_stat_string(dist, "haste"),
            "crit": generate_stat_string(dist, "crit")
        }
        rating_combinations.append(combination)
    print(f"Simming {len(rating_combinations)} number of combinations")
    output_file = f"{args.dir}/generated.simc"
    base_stats = f"""gear_crit_rating={int(stats_base)}
gear_haste_rating={int(stats_base)}
gear_mastery_rating={int(stats_base)}
gear_versatility_rating={int(stats_base)}\n\n"""
    with open(base_file, 'r', encoding="utf8") as b_file:
        data = b_file.read()
        b_file.close()
    with open(output_file, 'w+', encoding="utf8") as o_file:
        o_file.writelines(data)
        o_file.writelines(base_stats)
        for combo in rating_combinations:
            for stat in stats:
                o_file.write(
                    f'profileset."{combo.get("name")}"+={combo.get(stat)}\n')


def build_simc_file(talent_string, profile_name):
    """Returns output file name based on talent strings"""
    if talent_string:
        return f"profiles/{talent_string}/{profile_name}.simc"
    return f"profiles/{profile_name}.simc"


def replace_talents(talent_string, data):
    """Replaces the talents variable with the talent string given"""
    if "talents=" in data:
        data = re.sub(r'talents=.*', f"talents={talent_string}", data)
    else:
        data.replace(
            "spec=shadow", f"spec=shadow\ntalents={talent_string}")
    return data


def replace_gear(data):
    """replaces gear based on the default in config"""
    for slot in config["gear"]:
        if slot == "off_hand":
            if config["gear"][slot] != "":
                replacement_string = "off_hand=" + config["gear"][slot]
            else:
                replacement_string = ""
            data = data.replace(f"${{gear.{slot}}}", replacement_string)
        else:
            data = data.replace(f"${{gear.{slot}}}", config["gear"][slot])
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
        profiles = profiles + \
            f'profileset."{talent_name}"+=talents={talent_string}\n'

    return profiles


def build_profiles(talent_string, apl_string):
    # pylint: disable=R0912, too-many-locals, too-many-statements, line-too-long, too-many-nested-blocks, simplifiable-if-statement
    """build combination list e.g. pw_sa_1"""
    fight_styles = ["pw", "lm", "hm"]
    add_types = ["sa", "ba", "na"]
    targets = ["1", "2", "4"]
    overrides = ""
    with open("internal/overrides.simc", 'r', encoding="utf8") as overrides_file:
        overrides = overrides_file.read()
        overrides_file.close()
    combinations = [
        f"{fight}_{add}_{tar}" for fight in fight_styles for add in add_types for tar in targets
    ]
    sim_files = config["sims"][args.dir[:-1]]["files"]

    for sim_file in sim_files:
        with open(f"{args.dir}{sim_file}", 'r', encoding="utf8") as contents:
            data = contents.read()
            contents.close()
        if args.dungeons:
            combinations = utils.get_dungeon_combos()
        if talent_string:
            if args.dungeons:
                talents_expr = config["builds"][talent_string]["dungeons"]
            else:
                talents_expr = config["builds"][talent_string]["composite"]
        else:
            talents_expr = ''
        data = replace_gear(data)
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
            st_weight = find_weights(
                config["singleTargetWeights"]).get(profile) or 0
            two_target_weight = find_weights(
                config["twoTargetWeights"]).get(profile) or 0
            four_target_weight = find_weights(
                config["fourTargetWeights"]).get(profile) or 0
            if weight == 0 and st_weight == 0 and two_target_weight == 0 and four_target_weight == 0 and not args.dungeons:
                # print(f"Skipping profile {profile} weights are all 0.")
                continue

            sim_data = data
            # prefix the profile name with the base file name
            profile_name = f"{sim_file[:-5]}_{profile}"
            settings = build_settings(
                profile, config["sims"][args.dir[:-1]]["weights"], args.dungeons)

            # insert talents based on profile
            if talents_expr:
                if args.dungeons:
                    target_count = 0
                else:
                    target_count = int(profile[-1])
                if profile in config["singleTargetProfiles"]:
                    new_talents = config["builds"][talent_string]["single"]
                    sim_data = replace_talents(new_talents, sim_data)
                elif target_count == 2:
                    new_talents = config["builds"][talent_string]["2t"]
                    sim_data = replace_talents(new_talents, sim_data)
                elif target_count == 4:
                    new_talents = config["builds"][talent_string]["4t"]
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


if __name__ == '__main__':
    parser = utils.generate_parser('Generates sim profiles.')
    args = parser.parse_args()

    talents = utils.get_talents(args)

    APL = "default_actions=1"

    if args.apl:
        with open("internal/apl.simc", 'r', encoding="utf8") as file:
            APL = file.read()
            file.close()

    clear_out_folders(f'{args.dir}output/')
    clear_out_folders(f'{args.dir}profiles/')

    if args.dir[:-1] == 'stats':
        build_stats_files()

    if talents:
        for talent in talents:
            clear_out_folders(f'{args.dir}output/{talent}/')
            clear_out_folders(f'{args.dir}profiles/{talent}/')
            print(f"Building {talent} profiles...")
            build_profiles(talent, APL)
    else:
        print("Building default profiles...")
        build_profiles(None, APL)
