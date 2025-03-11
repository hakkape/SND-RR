#!/usr/bin/env python3
import argparse 
import sys
import os
from pathlib import Path

this_file_folder = Path(__file__).parent

sys.path.append(str(this_file_folder) + "/Applications/")
sys.path.append(str(this_file_folder) + "/Objects/")

from InstanceGenerator import InstanceGen
from InstanceSolver import SolveInstance
from OutputWriter import OutputWriter

instance_dict = {'GROUP_TIMES': 'critical_times', 'DP': 'designated_paths', 'REGIONAL': 'hub_and_spoke'}
reverse_instance_dict = {'critical_times': 'GROUP_TIMES', 'designated_paths': 'DP', 'hub_and_spoke': 'REGIONAL'}


def main(instance_type: str, instance_path: Path, statistics_path: Path, time_limit: float, gap_limit: float):
    folder = str('/Instances/' + instance_type + '/')
    family = reverse_instance_dict[instance_type]
    solve_Parameters = {'INSTANCE_FOLDER': folder, 'DP': False, 'REGIONAL': False, 'GROUP_TIMES': False, family: True,
                        'TIME_LIMIT': time_limit, 'OPTIMALITY_GAP': gap_limit}
    input_folder = str(this_file_folder) + folder
    
    # Note: it seems to me that only the arguments solve_Parameters, instance_folder (fully specifies the instance) and scenario (specifies if node or arc disc is used) are necessary, the input folder and SND_instance have no influence on anything
    # the input folder seems to be used to write statistics only, but i overrode this with the statistics path
    Instance = SolveInstance(solve_Parameters, input_folder, str(instance_path) + "/", 0, "arc_disc")
    OutputWriter(Instance, statistics_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solves instances by van dyk et al. with Delta = 1"
    )

    parser.add_argument(
        "type",
        metavar="TYPE",
        type=str,
        help="Type of instance to solve (options are 'ct' for critical_time, 'dp' for designated_path and 'hs' for hub_and_spoke)",
    )

    parser.add_argument(
        "flat_number",
        metavar="FLATNUMBER",
        type=int,
        help="Number of flat instance to solve",
    )
    parser.add_argument(
        "time_number",
        metavar="TIMENUMBER",
        type=int,
        help="Number of time instance to solve",
    )
    parser.add_argument(
        "-s",
        "--statistics",
        type=str,
        help="Path to folder in which statistics should be stored",
    )

    parser.add_argument(
        "-t",
        "--timelimit",
        type=float,
        help="Time limit for the solver in seconds",
        default=3600,
    )
    parser.add_argument(
        "-g", "--gaplimit", type=float, help="Gap limit for the solver", default=0.01
    )

    type_to_folder_name = {
        "ct": "critical_times",
        "dp": "designated_paths",
        "hs": "hub_and_spoke",
    }

    # -- Reading out the arguments the user entered --
    flat_number = parser.parse_args().flat_number
    time_number = parser.parse_args().time_number
    instance_type = parser.parse_args().type
    instance_type = type_to_folder_name[instance_type]
    top_level_path = Path(__file__).parent
    instance_path = (
        top_level_path
        / f"Instances/{instance_type}/Instance-{flat_number}/{time_number}/"
    )
    statistics_path = parser.parse_args().statistics
    if statistics_path is not None:
        statistics_path = (
            Path(statistics_path) / f"{instance_type}_{flat_number}_{time_number}.csv"
        )
        # create folder if it does not exist
        statistics_path.parent.mkdir(parents=True, exist_ok=True)
    time_limit = parser.parse_args().timelimit
    gap_limit = parser.parse_args().gaplimit

    # -- Calling main function --
    main(instance_type, instance_path, statistics_path, time_limit, gap_limit)

