"""
simulation.py
-------------
Dynamic simulation of aircraft landing.

Each round, one plane lands, the fuel of all remaining planes decreases by 1,
and any plane that reaches fuel <= 0 crashes before it can land.
The list is re-sorted every round because the situaton changes constantly.

Available functions :
    - simulate(planes, policy, algorithm) : runs the full simulation
    - print_report(report)                : prints the final summary
"""

import copy
from sorts import insertion_sort


# --------------------------------------------------------------
# MAIN SIMULATION
# --------------------------------------------------------------

def simulate(planes: list, policy, algorithm=insertion_sort) -> dict:
    """
    Simulates the landing of all aircraft using the given policy and algorithm.

    Each round :
      1. Check for crashes (fuel <= 0) before sorting
      2. Sort the remaining planes according to the policy
      3. The first plane in the list lands and is removed from the queue
      4. All remaining planes lose 1 unit of fuel

    Parameters
    ----------
    planes    : list of dict -- initial dataset (not modified)
    policy    : function(a1, a2) -> bool -- priority comparator
    algorithm : sorting function -- insertion_sort or selection_sort

    Returns
    -------
    dict :
        "landed"            : list of planes that landed succesfully
        "crashed"           : list of planes that ran out of fuel
        "log"               : list of strings, one line per event
        "total_comparisons" : total number of comparisons made accross all rounds
    """
    queue = copy.deepcopy(planes)
    landed = []
    crashed = []
    log = []
    total_comparisons = 0
    round_number = 1

    while queue:
        # check for crashes before doing anything else
        # any plane with fuel <= 0 is already doomed
        new_crashes = [p for p in queue if p["fuel"] <= 0]
        for plane in new_crashes:
            crashed.append(plane)
            queue.remove(plane)
            log.append(f"Round {round_number:>2} | CRASH       | {plane['id']:<8} | fuel={plane['fuel']}")

        if not queue:
            break

        # sort the remaining planes according to the curent policy
        sorted_queue, nb_comp = algorithm(queue, policy)
        total_comparisons += nb_comp
        queue = sorted_queue

        # the first plane in the sorted list lands
        plane = queue.pop(0)
        landed.append(plane)
        log.append(
            f"Round {round_number:>2} | LANDED      | {plane['id']:<8} | "
            f"fuel={plane['fuel']:<4} | medical={plane['medical']} | "
            f"technical={plane['technical_issue']} | diplo={plane['diplomatic_level']}"
        )

        # all remaining planes consume 1 unit of fuel while waiting
        for p in queue:
            p["fuel"] -= 1

        round_number += 1

    return {
        "landed": landed,
        "crashed": crashed,
        "log": log,
        "total_comparisons": total_comparisons,
    }


# --------------------------------------------------------------
# REPORT DISPLAY
# Prints a readable summary of the simulation results
# --------------------------------------------------------------

def print_report(report: dict) -> None:
    """
    Prints the full simulation report to the console.

    Parameters
    ----------
    report : dict -- result returned by simulate()
    """
    print("\n" + "=" * 65)
    print("  SIMULATION REPORT -- ROISSY AIRPORT")
    print("=" * 65)

    print("\n  FLIGHT LOG :")
    for line in report["log"]:
        print("    " + line)

    print("\n" + "-" * 65)
    print(f"  Planes landed successfully : {len(report['landed'])}")
    print(f"  Planes crashed             : {len(report['crashed'])}")
    print(f"  Total comparisons          : {report['total_comparisons']}")

    if report["crashed"]:
        # list the planes we failled to save
        print("\n  Crashed planes :")
        for p in report["crashed"]:
            print(f"    - {p['id']}  (fuel at crash : {p['fuel']})")

    print("=" * 65 + "\n")
