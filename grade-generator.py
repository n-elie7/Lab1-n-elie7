#!/usr/bin/env python3
"""
Grade Generator - Interactive grade calculation
"""

def validate_grade(grade):
    """Validate grade is a number between 0 and 100"""
    try:
        grade = float(grade)
        if 0 <= grade <= 100:
            return grade
        else:
            print("Error: Grade must be between 0 and 100.")
            return None
    except ValueError:
        print("Error: Grade must be a valid number.")
        return None

def validate_weight(weight):
    """Validate weight is a positive number"""
    try:
        weight = float(weight)
        if weight > 0:
            return weight
        else:
            print("Error: Weight must be a positive number.")
            return None
    except ValueError:
        print("Error: Weight must be a valid number.")
        return None

def validate_category(category):
    """Validate category is FA or SA"""
    category = category.strip().upper()
    if category in ['FA', 'SA']:
        return category
    else:
        print("Error: Category must be 'FA' (Formative) or 'SA' (Summative).")
        return None
