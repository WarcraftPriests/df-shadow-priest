# How to Run Talents
The easiest way to run the talent suite is by using the following command. This will automatically go through the steps outlined below.
```bash
python suite.py --talents --fresh
```
This runs the following commands in order:
1. `python profiles.py talents/`
2. `python sim.py talents/`
3. `python top.py`
4. `python profiles.py talents/ --dungeons`
5. `python sim.py talents/ --dungeons`
6. `python top.py`
7. `python profiles.py talents-top/`
8. `python sim.py talents-top/`
9. `python profiles.py talents-top/ --dungeons`
10. `python sim.py talents-top/ --dungeons`

If you would only like to run one half of the suite you can pass in `--composite` or `--dungeons` respectively.

## Why are there two talent folders?
The simple answer is to get a balance between running more combinations of talents and precision. We do a first pass of all the builds in `talents_duplicated` using Raidbots Smart iterations. This will use a range of iterations based on the error margins and drastically cuts down on how long things take to run by relying on margin of error ranges.

After the initial sim is complete we then take all the top builds from those runs based on a set of criteria (defined in `top.py`) and pull those into `internal/talents.yml`. These builds are then run a second time at higher precision in `talents-top/`.

## Running with a fresh set of TTM builds
If you would like to change out builds here are the TL;DR instructions:
1. Using TTM export builds using profilesets from the tool.
2. Empty out `talents.simc` and directly paste in the list of builds in that file.
3. Remove the comment from the top of the file if it exists.
4. Inside the `talents/` folder run `python ttm.py`.
5. You can then go back to the root directly to run `python suite.py --talents --fresh`.

# talents/ structure
- `base.simc`: Contains the base actor that will be used for all the profiles.
- `talents.simc`: Contains the base builds before they are duplicated straight from Talent Tree Manager syntax
- `talents_duplicated.simc`: Resulting duplicated file from `talents.simc` when we duplicate for things like DA -> VF and DR -> ME. (see below)
- `ttm.py`: Formats raw TTM exported data into a more readable format with duplicating for choice nodes.

## talents.simc
This is the main file that should be edited when you want to adjust builds run in the suite. Builds should be made using Talent Tree Manager with current defaults of:
- Intangibility
- Last Word
- Dark Ascension
- Distorted Reality
In a future commit this might not be hard-coded but it is for now.

This file should only have profilesets in it and nothing else.

The standard process is to make two sets of build setups with those default choices, one with Mind Flay and another with Mind Spike. This can be done however you want though and
is not strictly required. Once all base setups are directly copied into `talents.simc` you can move onto the `ttm.py` script.

## ttm.py
This script should be run after you have added your builds into `talents.simc`. You should remove the comment at the top of the file if present when generating new builds. This script first applies a set of rules to the talents found in `talents.simc`. The current rules are as follows:
- Don't add combos that waste points on Tormented Spirits without Yogg-Saron
- Don't add combos that waste points on Shadow Crash without Whispering Shadows
- Only allow you to have 1 node in the middle section not fully pointed in of the following: (maddening touch, dark evangelism, mind devourer, and phantasmal pathogen). (i.e. you can't have 1 point of Mind Devourer and 1 point of Dark Evangelism)
- Only allow you to have 1 node in the bottom section not fully pointed in of the following: (mastermind, screams of the void, and insidious ire).
- Don't add combos that have Deathspeaker talented but not Inescapable Torment or Mastermind
- Only allow builds with at least 9 points in the bottom section
- Only allow builds that have at least one Idol capstone talent selected

The rules above are meant to trim down builds so that we can get a wider array of diversity without hard-coding certain options. These should be tweaked as needed.

After the rules are applied the script then goes and does the duplication logic. Currently this is hard-coded to duplicate twice. Once for Distorted Reality -> Mind's Eye and another time for Dark Ascension -> Void Eruption. The resulting builds are all added to `talents_duplicated.simc`. This file should not be modified directly as it will get overwritten each time the script is run.

The script then takes `talents_duplicated.simc` and breaks it up into workable chunks suitable for submitting to Raidbots. Currently this is hard-coded at `4000` actors per file. Anecdotally Raidbots seems to choke around 5000-5500 actors so we set it a bit lower to make sure it doesn't crash + doesn't take too long to run. The longer a sim runs the more likely it is to be cancelled/restarted as Raidbots nodes restart. It puts these profiles into the `builds/` folder.

`top.py`, `profiles.py`, and `analyze.py` are all setup to handle these dynamic builds in their scripting for this folder ONLY. 