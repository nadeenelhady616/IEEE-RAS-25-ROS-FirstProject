"""
Registration module for the University Management System.
Handles registration logic between students and courses.
"""

import json
import os
from config import MAX_COURSES

class Registration:
    """
    Handles the registration process for students and courses.
    """
    
    @staticmethod
    def register_student(student_id, course_id, filename="data.json"):
        """
        Register a student for a course.
        
        Args:
            student_id (str): The ID of the student
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
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
            course_data = data["courses"][course_id]
            
            # Check if student is already registered for the course
            if course_id in student_data["courses"]:
                print(f"Student {student_id} is already registered for course {course_id}")
                return False
            
            # Check if student has reached the maximum number of courses
            if len(student_data["courses"]) >= MAX_COURSES:
                print(f"Student {student_id} has reached the maximum number of courses ({MAX_COURSES})")
                return False
            
            # Check if course is full
            if len(course_data["enrolled_students"]) >= course_data["max_students"]:
                print(f"Course {course_id} is full")
                return False
            
            # Register student for course
            student_data["courses"].append(course_id)
            course_data["enrolled_students"].append(student_id)
            
            # Initialize attendance record for the student in this course
            if "attendance" not in student_data:
                student_data["attendance"] = {}
            student_data["attendance"][course_id] = [0, 0]  # [attended, total]
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Student {student_id} successfully registered for course {course_id}")
            return True
        except Exception as e:
            print(f"Error registering student: {e}")
            return False
    
    @staticmethod
    def drop_course(student_id, course_id, filename="data.json"):
        """
        Drop a student from a course.
        
        Args:
            student_id (str): The ID of the student
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if the course was dropped, False otherwise
        """
        try:
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
            course_data = data["courses"][course_id]
            
            # Check if student is registered for the course
            if course_id not in student_data["courses"]:
                print(f"Student {student_id} is not registered for course {course_id}")
                return False
            
            # Drop course
            student_data["courses"].remove(course_id)
            course_data["enrolled_students"].remove(student_id)
            
            # Remove attendance record for this course
            if "attendance" in student_data and course_id in student_data["attendance"]:
                del student_data["attendance"][course_id]
            
            # Remove grade for this course if it exists
            if "grades" in student_data and course_id in student_data["grades"]:
                del student_data["grades"][course_id]
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Student {student_id} successfully dropped course {course_id}")
            return True
        except Exception as e:
            print(f"Error dropping course: {e}")
            return False
    
    @staticmethod
    def list_registered_courses(student_id, filename="data.json"):
        """
        List all courses a student is registered for.
        
        Args:
            student_id (str): The ID of the student
            filename (str): Path to the JSON file
            
        Returns:
            list: List of course IDs the student is registered for
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return []
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return []
            
            student_data = data["students"][student_id]
            courses = student_data["courses"]
            
            if not courses:
                print(f"Student {student_id} is not registered for any courses")
            else:
                print(f"Courses registered by student {student_id}:")
                for course_id in courses:
                    if "courses" in data and course_id in data["courses"]:
                        course_name = data["courses"][course_id]["course_name"]
                        print(f"  {course_id}: {course_name}")
                    else:
                        print(f"  {course_id}: Unknown course")
            
            return courses
        except Exception as e:
            print(f"Error listing registered courses: {e}")
            return []
    
    @staticmethod
    def list_enrolled_students(course_id, filename="data.json"):
        """
        List all students enrolled in a course.
        
        Args:
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            list: List of student IDs enrolled in the course
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return []
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return []
            
            course_data = data["courses"][course_id]
            students = course_data["enrolled_students"]
            
            if not students:
                print(f"No students enrolled in course {course_id}")
            else:
                print(f"Students enrolled in course {course_id}:")
                for student_id in students:
                    if "students" in data and student_id in data["students"]:
                        student_name = data["students"][student_id]["name"]
                        print(f"  {student_id}: {student_name}")
                    else:
                        print(f"  {student_id}: Unknown student")
            
            return students
        except Exception as e:
            print(f"Error listing enrolled students: {e}")
            return []


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
                    "courses": [],
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
                    "enrolled_students": []
                }
            }
        }
        
        with open("data.json", 'w') as file:
            json.dump(sample_data, file, indent=4)
    
    # Register a student for a course
    Registration.register_student("S12345", "CS101")
    
    # List registered courses for a student
    Registration.list_registered_courses("S12345")
    
    # List enrolled students in a course
    Registration.list_enrolled_students("CS101")
    
    # Drop a course
    Registration.drop_course("S12345", "CS101")

print("Registration module loaded successfully")