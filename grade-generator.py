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

def get_assignment_details():
    """Prompt user for assignment details with validation"""
    print("\n--- Enter Assignment Details ---")
    
    # Get assignment name
    name = input("Assignment Name: ").strip()
    while not name:
        print("Error: Assignment name cannot be empty.")
        name = input("\nAssignment Name: ").strip()
    
    # Get and validate category (must be FA/SA)
    category = None
    while category is None:
        category_input = input("Category (FA/SA): ").strip()
        category = validate_category(category_input)
    
    # Get and validate grade (must be 0-100 range)
    grade = None
    while grade is None:
        grade_input = input("Grade Obtained (0-100): ").strip()
        grade = validate_grade(grade_input)
    
    # Get and validate weight
    weight = None
    while weight is None:
        weight_input = input("Weight: ").strip()
        weight = validate_weight(weight_input)
    
    return {
        'name': name,
        'category': category,
        'grade': grade,
        'weight': weight
    }
