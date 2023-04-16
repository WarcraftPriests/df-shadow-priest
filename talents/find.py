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
            filler_types = ["Flay_DR_TS", "Spike_DR_TS", "Spike_DR",
                            "Spike_TS", "Flay_TS", "Flay_DR", "Spike", "Flay"]
            for f_type in filler_types:
                if f_type in profile_name:
                    results.append(
                        [row[1], profile_name.split("_")[0], f_type])
        file.close()

        for result in results:
            profile_name = result[0]
            da_or_vf = result[1]
            spike_or_flay = result[2]
            filler_types = ["Spike", "Flay", "Spike_TS", "Flay_TS",
                            "Spike_DR", "Flay_DR", "Spike_DR_TS", "Flay_DR_TS"]
            MATCH = False

            if da_or_vf in ["VF", "DA"] and spike_or_flay in filler_types:
                with open(f"{da_or_vf}-{spike_or_flay}.simc", 'r', encoding="utf8") as sim_file:
                    for line in sim_file:
                        if profile_name in line and args.match in line:
                            print(profile_name)
                            MATCH = True
                            break
                    sim_file.close()
            if MATCH:
                break
