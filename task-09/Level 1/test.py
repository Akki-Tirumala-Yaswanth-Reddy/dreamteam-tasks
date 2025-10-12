import pytest
import math
from schoolBounty import *

def test_calculate_gpa_empty_list():
    assert calculate_gpa([]) == 0

def test_calculate_gpa_4_0():
    assert calculate_gpa([95, 92, 98]) == 4.0

def test_calculate_gpa_2_0():
    assert calculate_gpa([55, 58, 52]) == 2.0


def test_calculate_gpa_1_0():
    assert calculate_gpa([45, 48, 42]) == 1.0


def test_calculate_gpa_boundary_90():
    assert calculate_gpa([90]) == 3.5  


def test_assign_scholarship_both_qualify():
    assert assign_scholarship(4.0, 80) == True


def test_assign_scholarship_gpa_too_low():
    assert assign_scholarship(3.0, 80) == False


def test_assign_scholarship_extracurricular_too_low():
    assert assign_scholarship(4.0, 60) == False


def test_assign_scholarship_both_too_low():
    assert assign_scholarship(3.0, 60) == False


def test_assign_scholarship_boundary_gpa():
    assert assign_scholarship(3.5, 80) == False 

def test_assign_scholarship_boundary_extracurricular():
    assert assign_scholarship(4.0, 70) == False  


def test_normalize_scores():
    assert normalize_scores([50, 100, 25]) == [0.5, 1.0, 0.25]


def test_normalize_scores_all_same():
    assert normalize_scores([100, 100, 100]) == [1.0, 1.0, 1.0]


def test_normalize_scores_single_one():
    assert normalize_scores([75]) == [1.0]


def test_normalize_scores_with_zero():
    assert normalize_scores([0, 50, 100]) == [0.0, 0.5, 1.0]


def test_find_top_student_clear_winner():
    students = [("Yaswanth", 95), ("Dheeru", 87), ("Sakai", 92)]
    assert find_top_student(students) == "Yaswanth"


def test_find_top_student_single_student():
    students = [("Sakai", 85)]
    assert find_top_student(students) == "Sakai"


def test_find_top_student_tie():
    students = [("Sakai", 90), ("Yaswanth", 90), ("Dheeru", 85)]
    result = find_top_student(students)
    assert result in ["Sakai", "Yaswanth"]  

def test_find_top_student_list_sorted():
    students = [("Sakai", 95), ("Dheeru", 90), ("Jin", 85)]
    assert find_top_student(students) == "Sakai"


def test_safe_divide_exact():
    assert safe_divide(10, 5) == 2


def test_safe_divide_rounds_up():
    assert safe_divide(10, 3) == 4  

def test_safe_divide_already_whole():
    assert safe_divide(20, 4) == 5


def test_safe_divide_by_one():
    assert safe_divide(7, 1) == 7


def test_safe_divide_small_result():
    assert safe_divide(1, 10) == 1  

def test_safe_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        safe_divide(10, 0)


def test_safe_divide_negative_numbers():
    assert safe_divide(-10, 3) == -3 