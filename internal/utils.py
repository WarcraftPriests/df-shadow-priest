"""stores utils that are shared between scripts"""
import argparse
import yaml

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_talents(args):
    """lookup talents based on current config"""
    if args.talents:
        talents = [args.talents]
    elif config["sims"][args.dir[:-1]]["builds"]:
        talents = config["builds"].keys()
    else:
        talents = []
    return talents


def get_simc_dir(talent, folder_name):
    """get proper directory based on talent options"""
    if talent:
        return f"{folder_name}/{talent}/"
    return f"{folder_name}/"


def generate_parser(description):
    """creates the shared argparser for sim.pu and profiles.py"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dir', help='Directory to generate profiles for.')
    parser.add_argument(
        '--dungeons', help='Run a dungeonsimming batch of sims.', action='store_true')
    parser.add_argument(
        '--talents', help='indicate talent build for output.', choices=config["builds"].keys())
    parser.add_argument(
        '--ptr', help='indicate if the sim should use ptr data.', action='store_true')
    parser.add_argument(
        '--apl', help='indicate if the sim should use the custom apl.', action='store_true')
    return parser


def get_dungeon_combos():
    """creates a list of the dungeon combinations"""
    season = config["dungeonSeason"]
    if season == 2:
        keys = ["bhh", "freehold", "hoi", "neltharus",
                "nelths", "ulda", "ur", "vtp"]
    else:
        keys = ["algethar", "azure", "cos", "hov",
                "nokhud", "rlp", "smbg", "temple"]
    affixes = ["fort", "tyran"]
    combos = [
        f"{key}-{affix}" for key in keys for affix in affixes]
    return combos
