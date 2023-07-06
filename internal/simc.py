"""local simc functions"""
import subprocess
import os
import time

def sim_local(simc_path, profile_location, output_location, iterations):
    """sim against a local simc instance"""
    location_list = output_location.split("/")
    logloc = output_location.replace("json", "log")
    with open(logloc, 'w', encoding="utf8") as file:
        try:
            subprocess.check_call(
                [
                    simc_path,
                    f"json2={output_location}",
                    f"iterations={iterations}",
                    profile_location
                ], stdout=file, stderr=file)
        except subprocess.CalledProcessError as ex:
            print(ex)
            print(f"-- {location_list[-1]} has an error. Skipping file.")
        file.close()
        time.sleep(1)
        os.remove(logloc)


def raidbots(simc_path, profile_location, simc_build, output_location, report_name, iterations):  # noqa: E501
    """just pass through to sim_local"""
    sim_local(simc_path, profile_location, output_location, iterations)
