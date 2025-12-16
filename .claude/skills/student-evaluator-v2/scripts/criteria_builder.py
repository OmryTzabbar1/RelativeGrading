"""
Criteria Builder Module
Manages the dynamic discovery and evolution of grading criteria.
"""

from typing import Dict, List, Any
import yaml


class DiscoveredCriteria:
    """
    Tracks quality dimensions discovered during sliding window analysis.

    Attributes:
        dimensions: Dictionary of discovered quality dimensions and their properties
        evolution_log: List tracking which student introduced each criterion
    """

    def __init__(self):
        """Initialize empty criteria structure."""
        self.dimensions: Dict[str, Any] = {}
        self.evolution_log: List[Dict[str, Any]] = []

    def add_dimension(self, name: str, properties: Dict[str, Any], discovered_by: str) -> None:
        """
        Add a new quality dimension to the criteria.

        Args:
            name: Dimension name (e.g., 'documentation', 'testing')
            properties: Dimension properties and thresholds
            discovered_by: Student who introduced this dimension
        """
        if name not in self.dimensions:
            self.dimensions[name] = properties
            self.evolution_log.append({
                'student': discovered_by,
                'dimension': name,
                'properties': properties.copy()
            })

    def update_dimension(self, name: str, new_properties: Dict[str, Any]) -> None:
        """
        Update existing dimension with new information.

        Args:
            name: Dimension name to update
            new_properties: New properties to merge into existing dimension
        """
        if name in self.dimensions:
            self.dimensions[name].update(new_properties)

    def has_dimension(self, name: str) -> bool:
        """
        Check if dimension already exists in criteria.

        Args:
            name: Dimension name to check

        Returns:
            True if dimension exists, False otherwise
        """
        return name in self.dimensions

    def get_dimension(self, name: str) -> Dict[str, Any]:
        """
        Get properties of a specific dimension.

        Args:
            name: Dimension name

        Returns:
            Dictionary of dimension properties, or empty dict if not found
        """
        return self.dimensions.get(name, {})

    def merge_features(self, features: Dict[str, Any], student_name: str) -> List[str]:
        """
        Merge newly discovered features into criteria.

        Args:
            features: Feature dictionary from analyze_project()
            student_name: Name of student whose features are being merged

        Returns:
            List of new dimension names that were added
        """
        new_dimensions = []

        for feature_name, feature_data in features.items():
            if not self.has_dimension(feature_name):
                self.add_dimension(feature_name, feature_data, student_name)
                new_dimensions.append(feature_name)
            else:
                # Update existing dimension with new information
                self.update_dimension(feature_name, feature_data)

        return new_dimensions

    def to_yaml(self) -> str:
        """
        Export criteria to YAML format.

        Returns:
            YAML string representation of criteria and evolution log
        """
        return yaml.dump({
            'criteria': self.dimensions,
            'evolution': self.evolution_log
        }, default_flow_style=False, sort_keys=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export criteria as dictionary.

        Returns:
            Dictionary with criteria and evolution data
        """
        return {
            'criteria': self.dimensions,
            'evolution': self.evolution_log
        }

    def get_dimension_count(self) -> int:
        """
        Get total number of discovered dimensions.

        Returns:
            Count of dimensions
        """
        return len(self.dimensions)

    def get_dimension_names(self) -> List[str]:
        """
        Get list of all dimension names.

        Returns:
            List of dimension names
        """
        return list(self.dimensions.keys())


def merge_criteria(criteria: DiscoveredCriteria, features: Dict[str, Any], student_name: str) -> List[str]:
    """
    Helper function to merge features into criteria.

    Args:
        criteria: DiscoveredCriteria object to update
        features: Features discovered from student project
        student_name: Name of student

    Returns:
        List of newly added dimension names
    """
    return criteria.merge_features(features, student_name)
