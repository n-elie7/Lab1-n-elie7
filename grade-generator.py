#!/usr/bin/env python3
"""
Grade Generator - Interactive grade calculation and CSV export tool
"""

def validate_grade(grade_str):
    """Validate grade is a number between 0 and 100"""
    try:
        grade = float(grade_str)
        if 0 <= grade <= 100:
            return grade
        else:
            print("Error: Grade must be between 0 and 100.")
            return None
    except ValueError:
        print("Error: Grade must be a valid number.")
        return None
