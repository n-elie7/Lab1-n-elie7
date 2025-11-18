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

def calculate_final_grade(assignments):
    """Calculate weighted grades, totals, GPA, and pass/fail status"""
    formative_total = 0
    summative_total = 0
    formative_weight_total = 0
    summative_weight_total = 0
    
    for assignment in assignments:
        weighted_grade = (assignment['grade'] / 100) * assignment['weight']
        
        if assignment['category'] == 'FA':
            formative_total += weighted_grade
            formative_weight_total += assignment['weight']
        else:  # SA
            summative_total += weighted_grade
            summative_weight_total += assignment['weight']
    
    total_grade = formative_total + summative_total
    gpa = (total_grade / 100) * 5.0
    
    # Pass/Fail logic: need >= 50% in both categories
    formative_pass = formative_total >= (formative_weight_total * 0.5) if formative_weight_total > 0 else True
    summative_pass = summative_total >= (summative_weight_total * 0.5) if summative_weight_total > 0 else True
    status = "PASS" if (formative_pass and summative_pass) else "FAIL"
    
    # Determine assignments to resubmit (grade < 50)
    resubmit = [a['name'] for a in assignments if a['grade'] < 50]
    
    return {
        'formative_total': formative_total,
        'summative_total': summative_total,
        'formative_weight_total': formative_weight_total,
        'summative_weight_total': summative_weight_total,
        'total_grade': total_grade,
        'gpa': gpa,
        'status': status,
        'resubmit': resubmit
    }
