"""main sim script to run sims"""

import sys
import platform
import re
import os
from os import listdir
import importlib
import yaml

from internal.weights import find_weights
from internal.sim_parser import parse_json
from internal.sim_parser import get_timestamp
from internal.analyze import analyze
from internal import utils

api_secrets_spec = importlib.util.find_spec("api_secrets")
local_secrets_spec = importlib.util.find_spec("local_secrets")

if api_secrets_spec:
    api_secrets = api_secrets_spec.loader.load_module()

if local_secrets_spec:
    local_secrets = local_secrets_spec.loader.load_module()

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_path(simc_build_version):
    """get path depending on local OS"""
    path_dict = local_secrets.simc_path
    if not path_dict:
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            return "simc"
        return "simc.exe"

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        return handle_path_darwin(path_dict[simc_build_version])
    return handle_path_win(path_dict[simc_build_version])


def handle_path_darwin(path):
    """find the proper path if using darwin based OS"""
    if path.endswith("/"):
        return f"{path}simc"
    return f"{path}/simc"


def handle_path_win(path):
    """find the proper path if using windows based OS"""
    if path.endswith("\\"):
        return f"{path}simc.exe"
    return f"{path}\\simc.exe"


def get_api_key(args, simc_build_version):
    """get api key from secret"""
    if args.local:
        executable = get_path(simc_build_version)

        if is_executable(executable):
            return executable
        print(
            f"{executable} not a valid executable please check your local_secrets.py and PATH")  # noqa: E501
        sys.exit()
    else:
        return api_secrets.api_key


def is_executable(path):
    """check if given path is an executable"""
    return os.path.isfile(path) and os.access(path, os.X_OK)


def run_sims(args, iterations, talent):
    """run sims with the given config"""
    if args.local:
        from internal.simc import raidbots
    else:
        from internal.api import raidbots
    simc_build = config["simcBuild"]
    print(f"Running sims on {simc_build} in {args.dir}")
    existing = listdir(
        args.dir + utils.get_simc_dir(talent, 'output'))
    profiles = listdir(
        args.dir + utils.get_simc_dir(talent, 'profiles'))
    count = 0

    for profile in profiles:
        print(profile)
        if args.dungeons:
            profile_name = profile
        else:
            profile_name = re.search(
                '((hm|lm|pw).+?(?=.simc)|dungeons.simc)', profile).group()
        count = count + 1
        if not args.dungeons:
            weight = find_weights(
                config["compositeWeights"]).get(profile_name) or 0
            weight += find_weights(config["singleTargetWeights"]
                                   ).get(profile_name) or 0
            weight += find_weights(config["twoTargetWeights"]
                                   ).get(profile_name) or 0
            weight += find_weights(config["threeTargetWeights"]
                                   ).get(profile_name) or 0
            weight += find_weights(config["fourTargetWeights"]
                                   ).get(profile_name) or 0
        elif args.dungeons:
            # could look this up in the future, need to fix profile_name
            weight = 1
        else:
            weight = 1
        print(f"Simming {count} out of {len(profiles)}.")
        output_name = profile.replace('simc', 'json')
        if output_name not in existing and weight > 0:
            output_location = args.dir + \
                utils.get_simc_dir(talent, 'output') + output_name
            profile_location = args.dir + \
                utils.get_simc_dir(talent, 'profiles') + profile
            # prefix the profile name with the base file name
            profile_name_with_dir = f"{args.dir}{profile_name}"
            raidbots(get_api_key(args, config["simcBuild"]), profile_location,
                     config["simcBuild"], output_location, profile_name_with_dir, iterations)  # noqa: E501
        elif weight == 0:
            print(f"-- {output_name} has a weight of 0. Skipping file.")
        else:
            print(f"-- {output_name} already exists. Skipping file.")


def convert_to_csv(args, weights, talent):
    """creates results/statweights.txt"""
    results_dir = args.dir + utils.get_simc_dir(talent, 'output')
    parse_json(results_dir, weights)


def analyze_data(args, talent, weights):
    """create results"""
    analyze(talent, args.dir, args.dungeons, weights, get_timestamp())


def main():
    """main function, runs and parses sims"""
    parser = utils.generate_parser("Parses a list of reports from Raidbots.")
    args = parser.parse_args()

    sys.path.insert(0, args.dir)

    # Download simc if needed
    if local_secrets and args.local and args.auto_download:
        from internal.auto_download import download_latest
        local_secrets.simc_path['latest'] = download_latest()
        # Additional temp swap to using the latest build
        config['simcBuild'] = 'latest'

    weights = config["sims"][args.dir[:-1]]["weights"]

    if args.iterations:
        iterations = args.iterations
    elif config["sims"][args.dir[:-1]].get("iterations"):
        iterations = config["sims"][args.dir[:-1]]["iterations"]
    else:
        iterations = str(config["defaultIterations"])

    talents = utils.get_talents(args)

    if talents:
        for talent in talents:
            print(f"Simming {talent} profiles...")
            run_sims(args, iterations, talent)
            convert_to_csv(args, weights, talent)
            analyze_data(args, talent, weights)
    else:
        print("Simming default profiles...")
        run_sims(args, iterations, None)
        convert_to_csv(args, weights, None)
        analyze_data(args, None, weights)


if __name__ == "__main__":
    main()
