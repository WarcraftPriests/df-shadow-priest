"""finds a specific talent build"""
# python find.py Single shadow_crash:1
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sim_type",
        help="which sim type to search through",
        choices=[
            "Single",
            "2T",
            "3T",
            "Composite",
            "Dungeons-Push",
            "Dungeons-Standard",
        ],
    )  # noqa: E501
    parser.add_argument("match", help="string to match for")
    parser.add_argument("matchtwo", help="string to match for")
    parser.add_argument("matchthree", help="string to match for")
    args = parser.parse_args()

    results = []

    with open(f"results/Results_{args.sim_type}.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # DA_yshaarj_cthun_20576876345295_Spike
            profile_name = row[1]
            MATCH = False
            with open("talents_duplicated.simc", "r", encoding="utf8") as sim_file:
                for line in sim_file:
                    if (
                        profile_name in line
                        and args.match in line
                        and args.matchtwo in line
                        and args.matchthree in line
                    ):  # noqa: E501
                        print(profile_name)
                        MATCH = True
                        break
                sim_file.close()
            if MATCH:
                break
