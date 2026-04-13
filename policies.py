"""
policies.py
-----------
Defines the priority POLICIES used to rank incomming aircraft.

Convention : policy(a1, a2) returns True if a1 should land before a2.

Available policies :
    - policy_fuel       : lowest fuel lands first
    - policy_medical    : medical emergency has priority
    - policy_diplomatic : highest diplomatic level lands first
    - policy_crisis     : full crisis hierarchy (recomended)
"""


# --------------------------------------------------------------
# POLICY 1 : FUEL -- the plane with the least fuel lands first
# --------------------------------------------------------------

def policy_fuel(a1: dict, a2: dict) -> bool:
    """
    Priority to the lowest fuel level.
    Tiebreak : diplomatic level (descending), then arrival time.

    Parameters : a1, a2 (dict) -- two aircraft from the dataset
    Returns    : bool -- True if a1 should land before a2
    """
    if a1["fuel"] != a2["fuel"]:
        return a1["fuel"] < a2["fuel"]
    # if fuel is equal we look at diplomatic importence
    if a1["diplomatic_level"] != a2["diplomatic_level"]:
        return a1["diplomatic_level"] > a2["diplomatic_level"]
    # last resort tiebreak is arrival time
    return a1.get("arrival_time", 0) < a2.get("arrival_time", 0)


# --------------------------------------------------------------
# POLICY 2 : MEDICAL -- planes with a medical emergency go first
# --------------------------------------------------------------

def policy_medical(a1: dict, a2: dict) -> bool:
    """
    Priority to planes with an onboard medical emergency.
    Tiebreak : lowest fuel, then arrival time.

    Parameters : a1, a2 (dict)
    Returns    : bool -- True if a1 should land before a2
    """
    if a1["medical"] != a2["medical"]:
        return a1["medical"]  # True comes before False
    if a1["fuel"] != a2["fuel"]:
        return a1["fuel"] < a2["fuel"]
    return a1.get("arrival_time", 0) < a2.get("arrival_time", 0)


# --------------------------------------------------------------
# POLICY 3 : DIPLOMATIC -- highest diplomatic level lands first
# --------------------------------------------------------------

def policy_diplomatic(a1: dict, a2: dict) -> bool:
    """
    Priority to the highest diplomatic level.
    Tiebreak : lowest fuel, then arrival time.

    Parameters : a1, a2 (dict)
    Returns    : bool -- True if a1 should land before a2
    """
    if a1["diplomatic_level"] != a2["diplomatic_level"]:
        return a1["diplomatic_level"] > a2["diplomatic_level"]
    if a1["fuel"] != a2["fuel"]:
        return a1["fuel"] < a2["fuel"]
    return a1.get("arrival_time", 0) < a2.get("arrival_time", 0)


# --------------------------------------------------------------
# POLICY 4 : CRISIS -- full hierarchy for crisis situations (recomended)
# Order : technical issue > medical > fuel > diplomatic > arrival time
# --------------------------------------------------------------

def policy_crisis(a1: dict, a2: dict) -> bool:
    """
    Full crisis hierarchy :
      1. Technical issue (technical_issue) -- most urgent, plane may be unflyable
      2. Medical emergency (medical) -- human life at risk
      3. Lowest fuel (fuel) -- avoids a crash due to fuel exaustion
      4. Highest diplomatic level (diplomatic_level) -- political tiebreak
      5. Earliest arrival time (arrival_time) -- final fairness tiebreak

    Parameters : a1, a2 (dict)
    Returns    : bool -- True if a1 should land before a2
    """
    # 1. technical issue is the most critical situaton
    if a1["technical_issue"] != a2["technical_issue"]:
        return a1["technical_issue"]  # True before False

    # 2. medical emergencys come right after
    if a1["medical"] != a2["medical"]:
        return a1["medical"]

    # 3. lowest fuel is most dangeros
    if a1["fuel"] != a2["fuel"]:
        return a1["fuel"] < a2["fuel"]

    # 4. higher diplomatic level gets priority when everything else is equal
    if a1["diplomatic_level"] != a2["diplomatic_level"]:
        return a1["diplomatic_level"] > a2["diplomatic_level"]

    # 5. arrival time as the last tiebreak, garantees a stable result
    return a1.get("arrival_time", 0) < a2.get("arrival_time", 0)