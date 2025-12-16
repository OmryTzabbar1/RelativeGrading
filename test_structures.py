"""
Manual test script for DiscoveredCriteria and StudentEvaluation classes.
Run this to verify Phase 1 data structures are working.
"""

import sys
sys.path.insert(0, '.')

from scripts.criteria_builder import DiscoveredCriteria
from scripts.final_evaluator import StudentEvaluation, calculate_relative_grade


def test_discovered_criteria():
    """Test DiscoveredCriteria class."""
    print("Testing DiscoveredCriteria class...")

    # Create instance
    criteria = DiscoveredCriteria()
    assert criteria.get_dimension_count() == 0, "Initial criteria should be empty"

    # Add documentation dimension
    criteria.add_dimension(
        'documentation',
        {'readme': {'present': True, 'lines': 200}},
        'student_alice'
    )
    assert criteria.has_dimension('documentation'), "Should have documentation dimension"
    assert criteria.get_dimension_count() == 1, "Should have 1 dimension"

    # Add testing dimension
    criteria.add_dimension(
        'testing',
        {'present': True, 'test_file_count': 5},
        'student_bob'
    )
    assert criteria.get_dimension_count() == 2, "Should have 2 dimensions"

    # Check evolution log
    assert len(criteria.evolution_log) == 2, "Should have 2 evolution entries"
    assert criteria.evolution_log[0]['student'] == 'student_alice'
    assert criteria.evolution_log[1]['student'] == 'student_bob'

    # Test to_dict
    data = criteria.to_dict()
    assert 'criteria' in data
    assert 'evolution' in data

    print("[PASS] DiscoveredCriteria tests passed")


def test_student_evaluation():
    """Test StudentEvaluation class."""
    print("\nTesting StudentEvaluation class...")

    # Create instance
    eval_obj = StudentEvaluation('student_alice', '/path/to/alice')
    assert eval_obj.student_name == 'student_alice'
    assert eval_obj.quality_score == 0.0

    # Create criteria
    criteria = DiscoveredCriteria()
    criteria.add_dimension('documentation', {'weight': 10}, 'test')
    criteria.add_dimension('testing', {'weight': 15}, 'test')

    # Create project features
    features = {
        'documentation': {'readme': {'present': True}},
        'testing': {'present': True}
    }

    # Calculate quality score
    score = eval_obj.calculate_quality_score(criteria, features)
    assert score > 0, "Quality score should be > 0"
    assert eval_obj.dimension_scores['documentation'] == 10.0
    assert eval_obj.dimension_scores['testing'] == 15.0

    # Test grade assignment
    eval_obj.set_grade(95)
    assert eval_obj.grade == 95

    # Test rank assignment
    eval_obj.set_rank(1)
    assert eval_obj.rank == 1

    print("[PASS] StudentEvaluation tests passed")


def test_relative_grading():
    """Test relative grading calculation."""
    print("\nTesting relative grading...")

    best_score = 100.0

    # Test best student (100%)
    grade = calculate_relative_grade(100.0, best_score)
    assert grade == 100, "Best student should get 100"

    # Test 95% of best
    grade = calculate_relative_grade(95.0, best_score)
    assert 90 <= grade <= 99, f"95% should be 90-99, got {grade}"

    # Test 80% of best
    grade = calculate_relative_grade(80.0, best_score)
    assert 75 <= grade <= 89, f"80% should be 75-89, got {grade}"

    # Test 60% of best
    grade = calculate_relative_grade(60.0, best_score)
    assert 60 <= grade <= 74, f"60% should be 60-74, got {grade}"

    print("[PASS] Relative grading tests passed")


def test_merge_features():
    """Test feature merging."""
    print("\nTesting feature merging...")

    criteria = DiscoveredCriteria()

    # First student adds documentation
    features1 = {
        'documentation': {'readme': {'present': True}},
        'testing': {'present': False}
    }
    new_dims = criteria.merge_features(features1, 'student_1')
    assert len(new_dims) == 2, "Should add 2 new dimensions"

    # Second student adds graphics (new) and documentation (existing)
    features2 = {
        'documentation': {'prd': {'present': True}},
        'graphics': {'image_count': 10}
    }
    new_dims = criteria.merge_features(features2, 'student_2')
    assert len(new_dims) == 1, "Should add 1 new dimension (graphics)"
    assert 'graphics' in new_dims

    assert criteria.get_dimension_count() == 3, "Should have 3 total dimensions"

    print("[PASS] Feature merging tests passed")


if __name__ == '__main__':
    print("=" * 60)
    print("Phase 1 Data Structures - Manual Test Suite")
    print("=" * 60)

    try:
        test_discovered_criteria()
        test_student_evaluation()
        test_relative_grading()
        test_merge_features()

        print("\n" + "=" * 60)
        print("All tests passed! [SUCCESS]")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
