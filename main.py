"""
main.py
-------
Entry point for the "58 Minutes to Live" project.

Runs in order :
  1. Dataset validation
  2. Utility functions demo (min fuel, emergencies)
  3. Landing order for each policy
  4. Algorithm comparison (selection vs insertion)
  5. Stress tests on growing traffic volumes
  6. Full dynamic simulation with final report
"""

import random
import copy

from APP_datasets import AVIONS_INITIAL
Dataset = AVIONS_INITIAL
from policies import policy_fuel, policy_medical, policy_diplomatic, policy_crisis
from sorts import selection_sort, insertion_sort, compare_algorithms
from simulation import simulate, print_report


# --------------------------------------------------------------
# REQUIRED FIELDS -- every plane in the dataset must have these
# --------------------------------------------------------------

REQUIRED_FIELDS = {"id", "fuel", "medical", "technical_issue", "diplomatic_level", "arrival_time"}


# --------------------------------------------------------------
# 1. DATASET VALIDATION
# Checks that all planes have the expected fields and coherent values
# --------------------------------------------------------------

def validate_dataset(planes: list) -> bool:
    """
    Verifies that every plane in the dataset has all required fields
    and that their values are coherent.

    Parameters : planes (list of dict)
    Returns    : bool -- True if the dataset is valid
    """
    valid = True
    for i, plane in enumerate(planes):
        missing = REQUIRED_FIELDS - plane.keys()
        if missing:
            print(f"  ERROR plane #{i} ({plane.get('id', '?')}) -- missing fields : {missing}")
            valid = False
        if not isinstance(plane.get("fuel"), (int, float)) or plane.get("fuel") < 0:
            print(f"  ERROR plane #{i} ({plane.get('id', '?')}) -- invalid fuel value : {plane.get('fuel')}")
            valid = False
        if not isinstance(plane.get("medical"), bool):
            print(f"  ERROR plane #{i} ({plane.get('id', '?')}) -- 'medical' must be a boolean")
            valid = False
        if not isinstance(plane.get("technical_issue"), bool):
            print(f"  ERROR plane #{i} ({plane.get('id', '?')}) -- 'technical_issue' must be a boolean")
            valid = False
        if not (1 <= plane.get("diplomatic_level", 0) <= 5):
            print(f"  ERROR plane #{i} ({plane.get('id', '?')}) -- diplomatic_level out of range [1-5]")
            valid = False
    if valid:
        print(f"  OK -- dataset is valid ({len(planes)} planes, all fields present)")
    return valid


# --------------------------------------------------------------
# 2. UTILITY FUNCTIONS
# Small helpers for debuging and validating the data
# --------------------------------------------------------------

def display_list(planes: list, title: str = "Plane list") -> None:
    """Prints a list of planes as a readable table."""
    print(f"\n  {'-'*58}")
    print(f"  {title}")
    print(f"  {'-'*58}")
    print(f"  {'ID':<8} {'Fuel':>5} {'Med':>6} {'Tech':>6} {'Diplo':>6} {'Arrival':>8}")
    for p in planes:
        print(
            f"  {p['id']:<8} {p['fuel']:>5} {str(p['medical']):>6} "
            f"{str(p['technical_issue']):>6} {p['diplomatic_level']:>6} "
            f"{p.get('arrival_time', '-'):>8}"
        )

def find_min_fuel(planes: list) -> dict:
    """Returns the plane with the lowest fuel. Usefull for quick sanity checks."""
    return min(planes, key=lambda p: p["fuel"])

def extract_emergencies(planes: list) -> list:
    """Returns all planes with a medical emergency or a technical issue."""
    return [p for p in planes if p["medical"] or p["technical_issue"]]


# --------------------------------------------------------------
# 3. TRAFFIC GENERATOR
# Generates a list of n planes for stress testing diferent scenarios
# --------------------------------------------------------------

def generate_traffic(n: int, scenario: str = "normal") -> list:
    """
    Generates n planes for a given scenario.

    Available scenarios :
        "normal"            : random mix of all situations
        "fuel_crisis"       : all planes are critically low on fuel
        "medical_crisis"    : high proportion of medical emergencys
        "diplomatic_summit" : all planes have high diplomatic level

    Parameters : n (int), scenario (str)
    Returns    : list of dict
    """
    planes = []
    for i in range(n):
        plane = {
            "id": f"{scenario[:2].upper()}{i:03}",
            "fuel": random.randint(5, 60),
            "medical": random.random() < 0.05,
            "technical_issue": random.random() < 0.05,
            "diplomatic_level": random.randint(1, 5),
            "arrival_time": round(19.40 + i * 0.01, 3),
        }
        # overide some fields depending on the scenario
        if scenario == "fuel_crisis":
            plane["fuel"] = random.randint(1, 15)
        elif scenario == "medical_crisis":
            plane["medical"] = random.random() < 0.5
        elif scenario == "diplomatic_summit":
            plane["diplomatic_level"] = random.randint(3, 5)

        planes.append(plane)
    return planes


# --------------------------------------------------------------
# 4. STRESS TESTS
# Compares both algorithms on growing traffic volumes
# --------------------------------------------------------------

def run_stress_tests() -> None:
    """
    Runs selection sort and insertion sort on datasets of increasing size
    to empiricaly observe the O(n2) complexity behavior.
    """
    print(f"\n  {'N':>5} | {'Selection (comp)':>18} | {'Insertion (comp)':>18} | {'Selection (ms)':>15} | {'Insertion (ms)':>14}")
    print(f"  {'-'*80}")

    for n in [10, 30, 50, 100]:
        traffic = generate_traffic(n, scenario="normal")
        results = compare_algorithms(traffic, policy_crisis)
        sel = results["selection"]
        ins = results["insertion"]
        print(
            f"  {n:>5} | {sel['comparisons']:>18} | {ins['comparisons']:>18} | "
            f"{sel['time_s'] * 1000:>14.3f} | {ins['time_s'] * 1000:>14.3f}"
        )


# --------------------------------------------------------------
# ENTRY POINT
# --------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + "#" * 65)
    print("  58 MINUTES TO LIVE -- Landing priority system")
    print("  Roissy Airport -- Crisis situation")
    print("#" * 65)

    # step 1 : make sure the dataset is usable before doing anything
    print("\n[1] DATASET VALIDATION")
    validate_dataset(Dataset)

    # step 2 : quick look at the most critical planes
    print("\n[2] KEY INFORMATION")
    min_fuel_plane = find_min_fuel(Dataset)
    print(f"  Plane with lowest fuel : {min_fuel_plane['id']} ({min_fuel_plane['fuel']} min remaining)")
    emergencies = extract_emergencies(Dataset)
    print(f"  Planes with emergencies : {[p['id'] for p in emergencies]}")

    # step 3 : show the landing order for each policy
    print("\n[3] LANDING ORDER PER POLICY")
    policies = {
        "FUEL":       policy_fuel,
        "MEDICAL":    policy_medical,
        "DIPLOMATIC": policy_diplomatic,
        "CRISIS":     policy_crisis,
    }
    for name, policy in policies.items():
        sorted_list, nb_comp = insertion_sort(Dataset, policy)
        ids = [p["id"] for p in sorted_list]
        print(f"\n  Policy {name} ({nb_comp} comparisons) :")
        print(f"  {' -> '.join(ids)}")

    # step 4 : compare the two sorting algoritms on diferent traffic sizes
    print("\n[4] STRESS TESTS -- selection sort vs insertion sort")
    run_stress_tests()

    # step 5 : run the full dynamic simulation with the crisis policy
    print("\n[5] DYNAMIC SIMULATION -- policy CRISIS + insertion sort")
    report = simulate(Dataset, policy_crisis, algorithm=insertion_sort)
    print_report(report)