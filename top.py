"""finds top talent builds"""
# python top.py [--analyze_only False, --top_matches 5, --match_jitter 2]

import argparse
import csv
import math
import os
import json
import yaml

from internal import utils
from internal.api import raidbots
from api_secrets import api_key

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_top_talents(results, combos, directory, matches, jitter):
    talent_names = []
    for result in results:
        builds = []
        with open(f"{directory}/Results_{result}.csv", "r", encoding="utf8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                builds.append(row[1])
        file.close()
        # get top x builds
        talent_names.extend(builds[1 : matches + 1])
        for combo in combos:
            count = 0
            for build in builds:
                filler = ""
                fillers = ["Spike_ME", "Spike_DR", "Flay_ME", "Flay_DR"]
                for name in fillers:
                    if name in build:
                        filler = name
                if combo[0] in build and filler == combo[1]:
                    talent_names.append(build)
                    count = count + 1
                    # add a buffer to get more diversity
                    if count >= jitter:
                        break
    return list(set(talent_names))


def filter_dungeon_type(combo):
    if "push" in combo:
        return True
    else:
        return False


def get_builds():
    cds = ["VF", "DA"]
    idols = [
        "yshaarj_cthun",
        "nzoth_yogg",
        "nzoth_cthun",
        "yogg_cthun",
        "nzoth_yogg_cthun",
        "cthun",
    ]
    combos = [f"{cd}_{idol}" for cd in cds for idol in idols]  # noqa: E501
    return combos


def find_spec_talents(talent):
    spec_talents = "not_found"
    with open("talents/talents_duplicated.simc", "r", encoding="utf8") as file:
        for line in file:
            if talent in line:
                spec_talents = line.split("+=")[1].replace('"', "").replace("\n", "")
                break
    file.close()
    if spec_talents == "not_found":
        print(f"{talent} not found")
        exit()
    return spec_talents


def get_base_actor():
    file_name = os.listdir("talents/profiles/")[0]
    with open(f"talents/profiles/{file_name}", "r", encoding="utf8") as file:
        ending_line = 27
        for num, line in enumerate(file, 1):
            if "main_hand" in line:
                ending_line = num
    file.close()
    with open(f"talents/profiles/{file_name}", "r", encoding="utf8") as file:
        head = [next(file) for _ in range(ending_line)]
    file.close()
    head.extend("\n")
    return head


def create_sim_file(base, talent_dictionary, batches):
    items = list(talent_dictionary.items())
    # clear out existing build files
    for filename in os.listdir("talents/top/"):
        if os.path.isfile(os.path.join("talents/top/", filename)):
            os.remove(os.path.join("talents/top/", filename))
    # raidbots limits us to 200 actors per sim
    for batch in range(batches):
        start = 0 + (199 * batch)
        end = 199 + (199 * batch)
        with open(
            f"talents/top/top_talents_{batch}.simc", "w", encoding="utf8"
        ) as file:
            file.writelines(base)
            for actor in items[start:end]:
                file.writelines([f'copy="{actor[0]}","Base"\n', f"{actor[1]}\n\n"])
            file.write("iterations=1")
        file.close()


def populate_talent_strings(name):
    talent_string_dictionary = {}
    f = open(f"{name}.json")
    data = json.load(f)
    f.close()
    for player in data["sim"]["players"]:
        if player["name"] != "Base":
            talent_string_dictionary[player["name"]] = player["talents"]
    return talent_string_dictionary


def populate_talents(talent_string_dictionary):
    with open("internal/talents.yml", "r") as file:
        talents = yaml.safe_load(file)
        custom_builds = talents["builds"]
        full_yaml = {"builds": custom_builds, "generated": talent_string_dictionary}
    file.close()
    with open("internal/talents.yml", "w") as file:
        yaml.dump(full_yaml, file)
    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--top_matches", nargs="?", default=5, type=int)
    parser.add_argument("--match_jitter", nargs="?", default=2, type=int)
    parser.add_argument("--analyze_only", nargs="?", default=False, type=bool)
    args = parser.parse_args()

    # Setup Vars
    build_configs = get_builds()
    combos = [
        (cd, filler)
        for cd in build_configs
        for filler in ["Spike_ME", "Flay_ME", "Spike_DR", "Flay_DR"]
    ]  # noqa: E501
    results = [
        "Single",
        "2T",
        "3T",
        "4T",
        "Composite",
        "Dungeons-Push",
        "Dungeons-Standard",
    ]
    push_results = list(filter(filter_dungeon_type, utils.get_dungeon_combos()))

    # Get aggregate results
    talent_names = get_top_talents(
        results, combos, "talents/results", args.top_matches, args.match_jitter
    )
    # Get individual push dungeon results
    dungeon_talent_names = get_top_talents(
        push_results, combos, "talents/results/dungeons/push", 2, 1
    )
    talent_names.extend(dungeon_talent_names)
    # De-duplicate again
    talent_names = list(set(talent_names))
    print(f"Found {len(talent_names)} top builds.")
    # exit()

    # Build Talent Dictionary
    talent_dictionary = {}
    for talent in talent_names:
        talent_dictionary[talent] = find_spec_talents(talent)

    # Get base actor data
    base = get_base_actor()

    # Create copy actor files we will run (top_talents_X.simc)
    batches = math.ceil(len(talent_dictionary) / 199)
    create_sim_file(base, talent_dictionary, batches)

    # run a sim at 1 iteration in raidbots
    ## must pass the API something for iterations, but we manually set this to 1 when building the file
    talent_string_dictionary = {}
    for batch in range(batches):
        name = f"talents/top/top_talents_{batch}"
        if not args.analyze_only:
            raidbots(
                api_key,
                f"{name}.simc",
                config["simcBuild"],
                f"{name}.json",
                name,
                "smart",
            )
        # pull out the results and find the talent id string per actor
        t = populate_talent_strings(name)
        talent_string_dictionary.update(t)

    # fill out internal/talents.yml with generated talents
    populate_talents(talent_string_dictionary)
