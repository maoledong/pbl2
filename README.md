# pbl2

# 58 Minutes to Live

A PBL project for the Advanced Algorithms 1 module at ESME.

The scenario is based on a crisis at Roissy airport. Two runways are closed, 24 planes are inbound, some are low on fuel, some have medical emergencys or technical issues. The goal is to build a Python module that decides the landing order depending on a priority policy.

---

## Project structure

```
projet_algo/
│
├── main.py            entry point, runs everything
├── policies.py        priority rules (POLICIES)
├── sorts.py           sorting algorithms (selection + insertion)
├── simulation.py      dynamic simulation round by round
├── APP_datasets.py    datasets provided by the teacher
└── README.md
```

---

## How to run

```bash
python main.py
```

This will run in order:
- dataset validation
- key informations (min fuel, emergencies)
- landing order for each policy
- stress tests on 10, 30, 50 and 100 planes
- full dynamic simulation with a final report

---

## Policies

We defined 4 differents policies. Each one is a comparator function that takes two planes and returns True if the first one should land before the second.

- policy_fuel : lowest fuel lands first
- policy_medical : medical emergency lands first
- policy_diplomatic : highest diplomatic level lands first
- policy_crisis : full crisis hierarchy (technical issue > medical > fuel > diplomatic > arrival time)

The policy is completly separated from the sorting algorithm. You can switch policy without touching the sort.

---

## Sorting algorithms

We implemented two quadratic sorts :

- insertion sort : O(n2), stable
- selection sort : O(n2), not stable

Both functions return the sorted list and the number of comparisons made. Insertion sort is prefered in the simulation because it is stable, wich means equal planes keep their original order.

---

## Stress tests

We tested both algorithms on increasing traffic volumes to observe the O(n2) behavior.

| N     | Selection (comp.) | Insertion (comp.) |
|-------|-------------------|-------------------|
| 10    | 45                | ~25 to 45         |
| 30    | 435               | ~200 to 435       |
| 50    | 1225              | ~600 to 1225      |
| 100   | 4950              | ~2500 to 4950     |

Insertion sort is faster on partialy sorted data, which hapens often in the dynamic simulation.

---

## Simulation

Each round :
1. Remaining planes are sorted according to the policy
2. The first plane lands and is removed from the queue
3. All other planes lose 1 unit of fuel
4. Any plane with fuel <= 0 crashes

The final report shows how many planes landed safely and how many crashed.

---

## Team

| Member | Role |
|--------|------|
| ...    | Policies and project structure |
| ...    | Sorting algorithms |
| ...    | Simulation and report |
| ...    | Testing and validation |
