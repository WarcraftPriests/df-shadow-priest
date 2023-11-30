"""run full suite of sims"""
import argparse
import csv
import os
import subprocess
import sys
import yaml


with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def call_process(process_args):
    """runs a process and constantly monitors for output"""
    subprocess.check_call(process_args, stdout=sys.stdout, stderr=subprocess.STDOUT)


def update_state(directory, sim_type, output_file, script):
    """updates state text file"""
    with open(output_file, "a+", encoding="utf8") as file:
        file.write(f"{directory},{sim_type},{script},\n")
        file.close()


def check_state(sim_dir, sim_type, output_file, script):
    """opens state file to see if the sim has been ran yet"""
    with open(output_file, "r", encoding="utf8") as file:
        sims = csv.reader(file, delimiter=",")
        for row in sims:
            if len(row) == 0:
                continue
            if row[0] == sim_dir and row[1] == sim_type and row[2] == script:
                return False
    return True


def generate_args(sim_dir, sim_type, script, args):
    """generates arguments for each script based on input"""
    arguments = ["python", script, sim_dir]

    if sim_type == "dungeons":
        arguments.append("--dungeons")

    if args.ptr:
        arguments.append("--ptr")

    if args.apl:
        arguments.append("--apl")

    if args.local:
        arguments.append("--local")

    if args.local:
        arguments.append("--auto_download")

    return arguments


def run_suite(sim_dir, sim_type, output_file, sim, args):
    """helper function to orchestrate other calls"""
    if check_state(sim_dir, sim_type, output_file, "profiles"):
        call_process(generate_args(sim_dir, sim_type, "profiles.py", args))
        update_state(sim_dir, sim_type, output_file, "profiles")

    if check_state(sim_dir, sim_type, output_file, "sim"):
        print(f"Running sim suite for {sim} - {sim_type}")
        call_process(generate_args(sim_dir, sim_type, "sim.py", args))
        update_state(sim_dir, sim_type, output_file, "sim")
        if sim == "talents" and args.talents:
            subprocess.check_call(
                ["python", "top.py"], stdout=sys.stdout, stderr=subprocess.STDOUT
            )


def main():
    """main function, runs sim suite"""
    output_file = "internal/suite.csv"

    parser = argparse.ArgumentParser(description="Sims full sim suite")
    parser.add_argument(
        "--exclude",
        help="Exclude certain sim folders from the suite run",
        choices=config["sims"].keys(),
        default=["apl", "talents", "talents-top"],
        nargs="+",
        required=False,
    )
    parser.add_argument("--fresh", help="restart suite from start", action="store_true")
    parser.add_argument(
        "--ptr", help="indicate if the sim should use ptr data.", action="store_true"
    )
    parser.add_argument(
        "--dungeons", help="only run the dungeon suite", action="store_true"
    )
    parser.add_argument(
        "--composite", help="only run the composite suite", action="store_true"
    )
    parser.add_argument(
        "--apl",
        help="indicate if the sim should use the custom apl.",
        action="store_true",
    )  # noqa: E501
    parser.add_argument(
        "--local",
        help="indicate if the sim should run locally (not recommended)",
        action="store_true",
    )
    parser.add_argument(
        "--auto_download",
        help="if local enabled will grab the latest simc package",
        action="store_true",
    )
    parser.add_argument(
        "--talents", help="only run talent folders", action="store_true"
    )
    args = parser.parse_args()

    if args.fresh or not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf8") as file:
            file.write("dir,type,sim,\n")
            file.close()

    for sim in config["sims"].keys():
        if args.talents:
            if sim not in ["talents", "talents-top"]:
                continue
        elif sim in args.exclude:
            continue
        sim_dir = f"{sim}/"

        # By default run Composite and Dungeons suite
        # Can pass in --dungeons to ONLY run the Dungeons suite
        # Can pass in --composite to ONLY run the Composite suite
        if not args.dungeons:
            run_suite(sim_dir, "composite", output_file, sim, args)
        if not args.composite:
            run_suite(sim_dir, "dungeons", output_file, sim, args)


if __name__ == "__main__":
    main()
