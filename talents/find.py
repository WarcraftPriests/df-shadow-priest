"""finds a specific talent build"""
# python find.py Single shadow_crash:1
import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sim_type', help='which sim type to search through',
                        choices=["Single", "2T", "4T", "Composite", "Dungeons"])
    parser.add_argument('match', help='string to match for')
    args = parser.parse_args()

    results = []

    with open(f"results/Results_{args.sim_type}.csv", 'r', encoding="utf8") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # DA_yshaarj_cthun_20576876345295_Spike
            profile_name = row[1]
            if profile_name[-2:] == "SC":
                results.append([row[1], profile_name.split(
                    "_")[0], profile_name.split("_")[-2] + "_SC"])
            else:
                results.append([row[1], profile_name.split("_")[
                               0], profile_name.split("_")[-1]])
        file.close()

        for result in results:
            profile_name = result[0]
            da_or_vf = result[1]
            spike_or_flay = result[2]
            MATCH = False

            if da_or_vf in ["VF", "DA"] and spike_or_flay in ["Spike", "Flay", "Spike_SC", "Flay_SC"]:
                with open(f"{da_or_vf}-{spike_or_flay}.simc", 'r', encoding="utf8") as sim_file:
                    for line in sim_file:
                        if profile_name in line and args.match in line:
                            print(profile_name)
                            MATCH = True
                            break
                    sim_file.close()
            if MATCH:
                break
