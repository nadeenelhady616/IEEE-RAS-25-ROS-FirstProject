"""
Grading module for the University Management System.
Handles grading operations for students in courses.
"""

import json
import os
from config import GRADE_POINTS

class Grading:
    """
    Handles grading operations for students in courses.
    """
    
    @staticmethod
    def assign_grade(student_id, course_id, grade, filename="data.json"):
        """
        Assign a grade to a student for a course.
        
        Args:
            student_id (str): The ID of the student
            course_id (str): The ID of the course
            grade (str): The grade to assign (e.g., 'A', 'B+')
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if grade assignment was successful, False otherwise
        """
        try:
            # Validate grade
            if grade not in GRADE_POINTS:
                print(f"Invalid grade for course {course_id}")
            # Validate grade
            if grade not in GRADE_POINTS:
                print(f"Invalid grade: {grade}. Valid grades are: {', '.join(GRADE_POINTS.keys())}")
                return False
            
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return False
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return False
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return False
            
            student_data = data["students"][student_id]
            
            # Check if student is enrolled in the course
            if course_id not in student_data["courses"]:
                print(f"Student {student_id} is not enrolled in course {course_id}")
                return False
            
            # Initialize grades if it doesn't exist
            if "grades" not in student_data:
                student_data["grades"] = {}
            
            # Assign grade
            student_data["grades"][course_id] = grade
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Assigned grade {grade} to student {student_id} for course {course_id}")
            return True
        except Exception as e:
            print(f"Error assigning grade: {e}")
            return False
    
    @staticmethod
    def get_grade(student_id, course_id=None, filename="data.json"):
        """
        Get grades for a student.
        
        Args:
            student_id (str): The ID of the student
            course_id (str, optional): The ID of the course (if None, get for all courses)
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary with grade information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return {}
            
            student_data = data["students"][student_id]
            
            # Check if grades exist
            if "grades" not in student_data:
                print(f"No grades for student {student_id}")
                return {}
            
            grades_data = student_data["grades"]
            
            if course_id:
                # Get grade for a specific course
                if course_id not in grades_data:
                    print(f"No grade for student {student_id} in course {course_id}")
                    return {}
                
                grade = grades_data[course_id]
                grade_point = GRADE_POINTS.get(grade, 0)
                
                print(f"Grade for student {student_id} in course {course_id}: {grade} ({grade_point} points)")
                return {course_id: {"grade": grade, "points": grade_point}}
            else:
                # Get grades for all courses
                result = {}
                print(f"Grades for student {student_id} in all courses:")
                
                for c_id, grade in grades_data.items():
                    grade_point = GRADE_POINTS.get(grade, 0)
                    result[c_id] = {"grade": grade, "points": grade_point}
                    
                    # Get course name if available
                    course_name = data["courses"][c_id]["course_name"] if c_id in data["courses"] else "Unknown Course"
                    
                    print(f"  {c_id} ({course_name}): {grade} ({grade_point} points)")
                
                return result
        except Exception as e:
            print(f"Error getting grade: {e}")
            return {}
    
    @staticmethod
    def calculate_gpa(student_id, filename="data.json"):
        """
        Calculate GPA for a student based on all courses.
        
        Args:
            student_id (str): The ID of the student
            filename (str): Path to the JSON file
            
        Returns:
            float: The calculated GPA
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return 0.0
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return 0.0
            
            student_data = data["students"][student_id]
            
            # Check if grades exist
            if "grades" not in student_data or not student_data["grades"]:
                print(f"No grades for student {student_id}")
                return 0.0
            
            grades_data = student_data["grades"]
            
            total_points = 0
            total_credits = 0
            
            for course_id, grade in grades_data.items():
                # Get course credits if available
                if course_id in data["courses"]:
                    course_credits = data["courses"][course_id].get("credits", 3)  # Default to 3 credits
                else:
                    course_credits = 3  # Default to 3 credits
                
                grade_point = GRADE_POINTS.get(grade, 0)
                total_points += grade_point * course_credits
                total_credits += course_credits
            
            if total_credits == 0:
                return 0.0
            
            gpa = total_points / total_credits
            print(f"GPA for student {student_id}: {gpa:.2f}")
            return gpa
        except Exception as e:
            print(f"Error calculating GPA: {e}")
            return 0.0
    
    @staticmethod
    def get_course_grades(course_id, filename="data.json"):
        """
        Get grades for all students in a course.
        
        Args:
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary mapping student IDs to grade information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return {}
            
            course_data = data["courses"][course_id]
            enrolled_students = course_data["enrolled_students"]
            
            if not enrolled_students:
                print(f"No students enrolled in course {course_id}")
                return {}
            
            result = {}
            print(f"Grades for all students in course {course_id}:")
            
            for student_id in enrolled_students:
                if student_id in data["students"]:
                    student_data = data["students"][student_id]
                    student_name = student_data["name"]
                    
                    if "grades" in student_data and course_id in student_data["grades"]:
                        grade = student_data["grades"][course_id]
                        grade_point = GRADE_POINTS.get(grade, 0)
                        
                        result[student_id] = {
                            "name": student_name,
                            "grade": grade,
                            "points": grade_point
                        }
                        
                        print(f"  {student_id} ({student_name}): {grade} ({grade_point} points)")
                    else:
                        result[student_id] = {
                            "name": student_name,
                            "grade": "Not graded",
                            "points": 0
                        }
                        
                        print(f"  {student_id} ({student_name}): Not graded")
            
            return result
        except Exception as e:
            print(f"Error getting course grades: {e}")
            return {}
    
    @staticmethod
    def get_grade_distribution(course_id, filename="data.json"):
        """
        Get grade distribution for a course.
        
        Args:
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary with grade distribution information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return {}
            
            course_data = data["courses"][course_id]
            enrolled_students = course_data["enrolled_students"]
            
            if not enrolled_students:
                print(f"No students enrolled in course {course_id}")
                return {}
            
            # Initialize grade distribution
            distribution = {grade: 0 for grade in GRADE_POINTS.keys()}
            distribution["Not graded"] = 0
            
            # Count grades
            for student_id in enrolled_students:
                if student_id in data["students"]:
                    student_data = data["students"][student_id]
                    
                    if "grades" in student_data and course_id in student_data["grades"]:
                        grade = student_data["grades"][course_id]
                        if grade in distribution:
                            distribution[grade] += 1
                    else:
                        distribution["Not graded"] += 1
            
            # Calculate percentages
            total_students = len(enrolled_students)
            percentages = {}
            
            for grade, count in distribution.items():
                percentage = (count / total_students * 100) if total_students > 0 else 0
                percentages[grade] = percentage
            
            # Print distribution
            print(f"Grade distribution for course {course_id}:")
            for grade, count in distribution.items():
                if count > 0:
                    percentage = percentages[grade]
                    print(f"  {grade}: {count} students ({percentage:.1f}%)")
            
            return {
                "distribution": distribution,
                "percentages": percentages,
                "total_students": total_students
            }
        except Exception as e:
            print(f"Error getting grade distribution: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Create a sample data.json file if it doesn't exist
    if not os.path.exists("data.json"):
        sample_data = {
            "students": {
                "S12345": {
                    "name": "John Doe",
                    "student_id": "S12345",
                    "level": "Sophomore",
                    "courses": ["CS101", "MATH201"],
                    "grades": {},
                    "attendance": {}
                },
                "S67890": {
                    "name": "Jane Smith",
                    "student_id": "S67890",
                    "level": "Freshman",
                    "courses": ["CS101"],
                    "grades": {},
                    "attendance": {}
                }
            },
            "courses": {
                "CS101": {
                    "course_id": "CS101",
                    "course_name": "Introduction to Computer Science",
                    "max_students": 30,
                    "credits": 4,
                    "professor_id": "P54321",
                    "enrolled_students": ["S12345", "S67890"]
                },
                "MATH201": {
                    "course_id": "MATH201",
                    "course_name": "Calculus I",
                    "max_students": 25,
                    "credits": 3,
                    "professor_id": "P98765",
                    "enrolled_students": ["S12345"]
                }
            }
        }
        
        with open("data.json", 'w') as file:
            json.dump(sample_data, file, indent=4)
    
    # Assign grades
    Grading.assign_grade("S12345", "CS101", "A")
    Grading.assign_grade("S67890", "CS101", "B+")
    Grading.assign_grade("S12345", "MATH201", "A-")
    
    # Get grades for a student
    Grading.get_grade("S12345")
    
    # Calculate GPA
    Grading.calculate_gpa("S12345")
    
    # Get grades for all students in a course
    Grading.get_course_grades("CS101")
    
    # Get grade distribution for a course
    Grading.get_grade_distribution("CS101")

print("Grading module loaded successfully")