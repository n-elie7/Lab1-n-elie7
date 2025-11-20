#!/usr/bin/python3
"""
Grade Generator Calculator System
"""

import csv
import sys


def validate_grade(grade):
    """Validate grade is a number between 0 and 100"""
    try:
        grade = float(grade)
        if 0 <= grade <= 100:
            return int(grade)
        else:
            print("Oops: Grade must be between 0 and 100.")
            return None
    except ValueError:
        print("Oops: Grade must be a valid number.")
        return None


def validate_weight(weight):
    """Validate weight is a positive number"""
    try:
        weight = float(weight)
        if weight > 0:
            return int(weight)
        else:
            print("Oops: Weight must be a positive number.")
            return None
    except ValueError:
        print("Oops: Weight must be a valid number.")
        return None


def validate_category(category):
    """Validate category is FA or SA"""
    category = category.strip().upper()
    if category in ["FA", "SA"]:
        return category
    else:
        print("Oops: Category must be 'FA' (Formative) or 'SA' (Summative).")
        return None


def get_assignment_details():
    """Prompt user for assignment details with validation"""
    print("\n--- Enter Assignment Details ---")

    # Get assignment name
    name = input("Assignment Name: ").strip()
    while not name:
        print("Oops: Assignment name cannot be empty.")
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

    return {"name": name, "category": category, "grade": grade, "weight": weight}


def calculate_final_grade(assignments):
    """Calculate weighted grades, totals, GPA, and pass/fail status"""
    formative_total = 0
    summative_total = 0
    formative_weight_total = 0
    summative_weight_total = 0

    for assignment in assignments:
        weighted_grade = (assignment["grade"] / 100) * assignment["weight"]

        if assignment["category"] == "FA":
            formative_total += weighted_grade
            formative_weight_total += assignment["weight"]
        else:  # SA
            summative_total += weighted_grade
            summative_weight_total += assignment["weight"]

    total_grade = formative_total + summative_total
    gpa = (total_grade / 100) * 5.0

    # Pass/Fail logic: need >= 50% in both categories
    formative_pass = None
    summative_pass = None

    if formative_weight_total > 0:
        formative_pass = formative_total >= (formative_weight_total * 0.5)
    if summative_weight_total > 0:
        summative_pass = summative_total >= (summative_weight_total * 0.5)

    status = "PASS" if (formative_pass and summative_pass) else "FAIL"

    # Determine assignments to resubmit
    failed_formative = []

    for assignment in assignments:
        if assignment["category"] == "FA" and assignment["grade"] < 50:
            failed_formative.append(assignment)

    if not failed_formative:
        resubmit = []
    elif len(failed_formative) == 1:
        # Only one failed FA assignment - resubmit that one
        resubmit = [failed_formative[0]["name"]]
    else:
        # Multiple failed FA assignments - find highest weight
        max_weight = max(assignment["weight"] for assignment in failed_formative)
        max_weight_assignments = [
            assignment
            for assignment in failed_formative
            if assignment["weight"] == max_weight
        ]

        if len(max_weight_assignments) == 1:
            # One assignment with highest weight
            resubmit = [max_weight_assignments[0]["name"]]
        else:
            # Multiple assignments with same highest weight - show all
            resubmit = [assignment["name"] for assignment in max_weight_assignments]

    return {
        "formative_total": formative_total,
        "summative_total": summative_total,
        "formative_weight_total": formative_weight_total,
        "summative_weight_total": summative_weight_total,
        "total_grade": total_grade,
        "gpa": gpa,
        "status": status,
        "resubmit": resubmit,
    }


def print_results(results):
    """Print grade summary to console"""

    print("\n" + "-" * 31)
    print("\n--- RESULTS ---")
    print(
        f"Total Formative:  {results['formative_total']:.2f} / {int(results['formative_weight_total'])}"
    )
    print(
        f"Total Summative:  {results['summative_total']:.2f} / {int(results['summative_weight_total'])}"
    )

    out_of = int(results["formative_weight_total"] + results["summative_weight_total"])

    print("\n" + "-" * 30)
    print(f"Total Grade:       {results['total_grade']:.2f} / {out_of}")
    print(f"GPA:               {results['gpa']:.4f}")
    print(f"Status:            {results['status']}")

    if results["resubmit"]:
        for assignment in results["resubmit"]:
            print(f"Resubmission:      {assignment}")
    else:
        print("\nNo assignments to resubmit.")

    print("\n")


def save_to_csv(assignments, filename="grades.csv"):
    """Save assignments to CSV file"""
    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Assignment", "Category", "Grade", "Weight"])

            for assignment in assignments:
                writer.writerow(
                    [
                        assignment["name"],
                        assignment["category"],
                        assignment["grade"],
                        assignment["weight"],
                    ]
                )

        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


def main():
    """Main program loop"""
    print("=" * 60)
    print(" " * 15 + "GRADE GENERATOR CALCULATOR")
    print("=" * 60)
    print("\nThis tool will help you calculate your final grade.")
    print("You can enter multiple assignments with their details.\n")

    assignments = []

    while True:
        assignment = get_assignment_details()

        if assignment:
            assignments.append(assignment)
            print(f"\nAssignment '{assignment['name']}' added successfully!")

        # Ask if user wants to add another assignment
        while True:
            choice = input("\nAdd another assignment? (y/n): ").strip().lower()
            if choice in ["y", "n", "yes", "no"]:
                break
            print("Please enter 'y' or 'n'.")

        if choice in ["n", "no"]:
            break

    if not assignments:
        print("\nNo assignments entered. Exiting.")
        sys.exit(0)

    # Calculate results
    results = calculate_final_grade(assignments)

    # Print results
    print_results(results)

    # Save to CSV
    save_to_csv(assignments)


if __name__ == "__main__":
    main()
