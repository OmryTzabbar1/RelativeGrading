#!/usr/bin/env python3
"""
Assignment-Specific Calibration Profiles

Different assignments emphasize different skills.
This module provides assignment profiles that adjust criteria weights
based on assignment focus areas.
"""

import json
from pathlib import Path


# Define assignment profiles
ASSIGNMENT_PROFILES = {
    "WorkSubmissions04": {
        "name": "Multi-Agent Tour Guide (Parallel Processing)",
        "description": "Multi-agent orchestration with parallel processing focus",
        "focus_areas": ["CodeQuality", "Testing", "DevOps", "Planning"],
        "weight_multipliers": {
            "CodeQuality": 1.5,      # 50% more important
            "Testing": 1.3,          # 30% more important
            "DevOps": 1.2,           # 20% more important
            "Planning": 1.1,         # 10% more important
            "Documentation": 1.0,    # Standard
            "Research": 0.9,         # 10% less important
            "Business": 0.8,         # 20% less important
            "Visuals": 0.9,          # 10% less important
        },
        "required_criteria": [
            "Unit_Tests",
            "README",
            "Architecture_Documentation"
        ],
        "bonus_criteria": [
            "CI/CD_Pipeline",
            "Docker_Containerization",
            "Pre_Commit_Hooks",
            "Test_Coverage_Metrics"
        ]
    },

    "WorkSubmissions05": {
        "name": "RAG & Context Window Laboratory",
        "description": "Research-focused assignment on RAG systems and context windows",
        "focus_areas": ["Research", "Planning", "Implementation"],
        "weight_multipliers": {
            "Research": 1.6,         # 60% more important - Cost Analysis critical
            "Planning": 1.4,         # 40% more important - Requirements important
            "Documentation": 1.2,    # 20% more important - Usage guides critical
            "Testing": 1.0,          # Standard
            "CodeQuality": 0.7,      # 30% less important - Less emphasis
            "DevOps": 0.8,           # 20% less important
            "Business": 1.3,         # 30% more important - Cost analysis
            "Visuals": 0.9,          # 10% less important
        },
        "required_criteria": [
            "Cost_Analysis",
            "Architecture_Documentation",
            "README"
        ],
        "bonus_criteria": [
            "Jupyter_Notebooks",
            "Data_Visualization",
            "Performance_Benchmarking",
            "User_Research"
        ]
    },

    "WorkSubmissions06": {
        "name": "Experimental Software Project",
        "description": "Research and experimental development project",
        "focus_areas": ["Research", "Visuals", "Testing", "CodeQuality"],
        "weight_multipliers": {
            "Research": 1.5,         # 50% more important
            "Visuals": 1.4,          # 40% more important - Data viz critical
            "Testing": 1.3,          # 30% more important
            "CodeQuality": 1.2,      # 20% more important
            "Planning": 1.1,         # 10% more important
            "Documentation": 1.0,    # Standard
            "DevOps": 0.9,           # 10% less important
            "Business": 0.8,         # 20% less important
        },
        "required_criteria": [
            "README",
            "Unit_Tests",
            "Architecture_Documentation"
        ],
        "bonus_criteria": [
            "Jupyter_Notebooks",
            "Screenshots",
            "Data_Visualization",
            "Experimental_Research"
        ]
    }
}


def detect_assignment_type(folder_path):
    """
    Auto-detect assignment type from folder name

    Args:
        folder_path: Path to WorkSubmissions folder

    Returns:
        str: Assignment key (e.g., "WorkSubmissions04") or None
    """
    folder_name = Path(folder_path).name

    # Direct match
    if folder_name in ASSIGNMENT_PROFILES:
        return folder_name

    # Partial match
    for assignment_key in ASSIGNMENT_PROFILES.keys():
        if assignment_key.lower() in folder_name.lower():
            return assignment_key

    return None


def get_assignment_profile(assignment_key):
    """
    Get assignment profile by key

    Args:
        assignment_key: Assignment identifier (e.g., "WorkSubmissions04")

    Returns:
        dict: Assignment profile or None if not found
    """
    return ASSIGNMENT_PROFILES.get(assignment_key)


def apply_assignment_profile(criteria_graph, assignment_key):
    """
    Apply assignment-specific weight adjustments to criteria graph

    Args:
        criteria_graph: Dict with metadata and criteria
        assignment_key: Assignment identifier

    Returns:
        dict: Updated criteria graph with adjusted weights
    """

    profile = get_assignment_profile(assignment_key)
    if not profile:
        print(f"Warning: No profile found for {assignment_key}, using default weights")
        return criteria_graph

    print(f"\nApplying assignment profile: {profile['name']}")
    print(f"Focus areas: {', '.join(profile['focus_areas'])}")

    # Track adjustments for reporting
    adjustments = {}

    # Apply weight multipliers by category
    for criterion_key, criterion_data in criteria_graph["criteria"].items():
        category = criterion_data.get("category", "Uncategorized")
        multiplier = profile["weight_multipliers"].get(category, 1.0)

        if multiplier != 1.0:
            old_weight = criterion_data["weight"]
            criterion_data["weight"] = old_weight * multiplier

            if category not in adjustments:
                adjustments[category] = {
                    "multiplier": multiplier,
                    "criteria_affected": 0,
                    "total_weight_change": 0
                }

            adjustments[category]["criteria_affected"] += 1
            adjustments[category]["total_weight_change"] += (criterion_data["weight"] - old_weight)

    # Mark required criteria
    for req_criterion in profile.get("required_criteria", []):
        # Normalize criterion name (handle variations)
        normalized_req = req_criterion.replace("_", " ").lower()

        for criterion_key, criterion_data in criteria_graph["criteria"].items():
            normalized_crit = criterion_key.replace("_", " ").lower()

            if normalized_req in normalized_crit or normalized_crit in normalized_req:
                criterion_data["required"] = True
                # Missing required criteria = severe penalty
                criterion_data["required_penalty"] = -5.0

    # Mark bonus criteria (extra credit)
    for bonus_criterion in profile.get("bonus_criteria", []):
        normalized_bonus = bonus_criterion.replace("_", " ").lower()

        for criterion_key, criterion_data in criteria_graph["criteria"].items():
            normalized_crit = criterion_key.replace("_", " ").lower()

            if normalized_bonus in normalized_crit or normalized_crit in normalized_bonus:
                criterion_data["bonus"] = True
                # Bonus criteria give extra weight
                criterion_data["weight"] = criterion_data["weight"] * 1.2

    # Add profile metadata
    criteria_graph["metadata"]["assignment_profile"] = {
        "key": assignment_key,
        "name": profile["name"],
        "description": profile["description"],
        "focus_areas": profile["focus_areas"],
        "adjustments_applied": adjustments
    }

    # Print summary
    print("\nWeight adjustments applied:")
    for category, adj_data in sorted(adjustments.items(), key=lambda x: x[1]["multiplier"], reverse=True):
        mult = adj_data["multiplier"]
        count = adj_data["criteria_affected"]
        change = adj_data["total_weight_change"]
        direction = "increased" if change > 0 else "decreased"
        print(f"  {category}: {mult:.1f}x multiplier ({count} criteria, {direction} by {abs(change):.2f} total weight)")

    return criteria_graph


def calculate_profile_adjusted_score(student_criteria, criteria_graph, assignment_key):
    """
    Calculate student score with profile adjustments

    Args:
        student_criteria: List of criteria student has
        criteria_graph: Criteria graph with weights
        assignment_key: Assignment identifier

    Returns:
        dict: Score breakdown with profile adjustments
    """

    profile = get_assignment_profile(assignment_key)
    if not profile:
        # No profile, use standard scoring
        raw_score = sum(
            criteria_graph["criteria"][c]["weight"]
            for c in student_criteria
            if c in criteria_graph["criteria"]
        )
        return {
            "raw_score": raw_score,
            "adjusted_score": raw_score,
            "profile_applied": False
        }

    # Calculate with profile adjustments
    raw_score = 0
    bonus_score = 0
    penalty_score = 0

    for criterion in student_criteria:
        if criterion in criteria_graph["criteria"]:
            crit_data = criteria_graph["criteria"][criterion]
            raw_score += crit_data["weight"]

            # Add bonus if applicable
            if crit_data.get("bonus"):
                bonus_score += crit_data["weight"] * 0.2  # 20% bonus

    # Check for missing required criteria
    for req_criterion in profile.get("required_criteria", []):
        normalized_req = req_criterion.replace("_", " ").lower()
        found = False

        for student_crit in student_criteria:
            normalized_crit = student_crit.replace("_", " ").lower()
            if normalized_req in normalized_crit or normalized_crit in normalized_req:
                found = True
                break

        if not found:
            penalty_score += 5.0  # Missing required criterion

    adjusted_score = raw_score + bonus_score - penalty_score

    return {
        "raw_score": raw_score,
        "bonus_score": bonus_score,
        "penalty_score": penalty_score,
        "adjusted_score": adjusted_score,
        "profile_applied": True,
        "profile_name": profile["name"]
    }


def export_profile_summary(assignment_key, output_path):
    """Export assignment profile summary as JSON"""

    profile = get_assignment_profile(assignment_key)
    if not profile:
        return False

    with open(output_path, 'w') as f:
        json.dump(profile, f, indent=2)

    return True


def list_available_profiles():
    """List all available assignment profiles"""

    print("Available Assignment Profiles:")
    print("=" * 80)

    for key, profile in ASSIGNMENT_PROFILES.items():
        print(f"\n{key}:")
        print(f"  Name: {profile['name']}")
        print(f"  Description: {profile['description']}")
        print(f"  Focus: {', '.join(profile['focus_areas'])}")

        print(f"  Weight Multipliers:")
        for category, mult in sorted(profile['weight_multipliers'].items(), key=lambda x: x[1], reverse=True):
            if mult > 1.0:
                print(f"    {category}: {mult:.1f}x (emphasized)")
            elif mult < 1.0:
                print(f"    {category}: {mult:.1f}x (de-emphasized)")

        print(f"  Required: {', '.join(profile.get('required_criteria', []))}")
        print(f"  Bonus: {', '.join(profile.get('bonus_criteria', []))}")


if __name__ == "__main__":
    # Test the profiles
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_available_profiles()
        elif sys.argv[1] == "export":
            if len(sys.argv) > 3:
                assignment_key = sys.argv[2]
                output_path = sys.argv[3]
                if export_profile_summary(assignment_key, output_path):
                    print(f"Exported {assignment_key} profile to {output_path}")
                else:
                    print(f"Profile not found: {assignment_key}")
            else:
                print("Usage: python assignment_profiles.py export <assignment_key> <output_path>")
        else:
            assignment_key = sys.argv[1]
            profile = get_assignment_profile(assignment_key)
            if profile:
                print(json.dumps(profile, indent=2))
            else:
                print(f"Profile not found: {assignment_key}")
    else:
        list_available_profiles()
