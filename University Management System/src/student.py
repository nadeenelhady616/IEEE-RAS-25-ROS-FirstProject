"""
Student module for the University Management System.
Handles student data and operations.
"""

import json
import os
from config import MAX_COURSES, GRADE_POINTS

class Student:
    """
    Represents a student in the university system.
    """
    
    def __init__(self, name, student_id, level):
        """
        Initialize a new Student instance.
        
        Args:
            name (str): The student's full name
            student_id (str): Unique identifier for the student
            level (str): Academic level (e.g., 'Freshman', 'Sophomore')
        """
        self.name = name
        self.student_id = student_id
        self.level = level
        self.courses = []
        self.grades = {}  # course_id: grade
        self.attendance = {}  # course_id: [attended_classes, total_classes]
    
    def register_course(self, course_id):
        """
        Register the student for a course.
        
        Args:
            course_id (str): The ID of the course to register for
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        if len(self.courses) >= MAX_COURSES:
            print(f"Cannot register for more than {MAX_COURSES} courses")
            return False
        
        if course_id in self.courses:
            print(f"Already registered for course {course_id}")
            return False
        
        self.courses.append(course_id)
        self.attendance[course_id] = [0, 0]  # [attended, total]
        print(f"Successfully registered for course {course_id}")
        return True
    
    def drop_course(self, course_id):
        """
        Drop a course the student is registered for.
        
        Args:
            course_id (str): The ID of the course to drop
            
        Returns:
            bool: True if the course was dropped, False otherwise
        """
        if course_id not in self.courses:
            print(f"Not registered for course {course_id}")
            return False
        
        self.courses.remove(course_id)
        if course_id in self.grades:
            del self.grades[course_id]
        if course_id in self.attendance:
            del self.attendance[course_id]
        print(f"Successfully dropped course {course_id}")
        return True
    
    def view_courses(self):
        """
        View all courses the student is registered for.
        
        Returns:
            list: List of course IDs
        """
        if not self.courses:
            print("Not registered for any courses")
        else:
            print(f"Registered courses: {', '.join(self.courses)}")
        return self.courses
    
    def view_grades(self):
        """
        View grades for all courses.
        
        Returns:
            dict: Dictionary mapping course IDs to grades
        """
        if not self.grades:
            print("No grades available")
        else:
            for course_id, grade in self.grades.items():
                print(f"Course: {course_id}, Grade: {grade}")
        return self.grades
    
    def calculate_gpa(self):
        """
        Calculate the student's GPA based on current grades.
        
        Returns:
            float: The calculated GPA
        """
        if not self.grades:
            print("No grades available to calculate GPA")
            return 0.0
        
        total_points = 0
        total_courses = 0
        
        for course_id, grade in self.grades.items():
            if grade in GRADE_POINTS:
                total_points += GRADE_POINTS[grade]
                total_courses += 1
        
        if total_courses == 0:
            return 0.0
        
        gpa = total_points / total_courses
        print(f"Current GPA: {gpa:.2f}")
        return gpa
    
    def view_attendance(self, course_id=None):
        """
        View attendance for a specific course or all courses.
        
        Args:
            course_id (str, optional): The course ID to view attendance for
            
        Returns:
            dict: Dictionary with attendance information
        """
        if course_id:
            if course_id not in self.attendance:
                print(f"No attendance records for course {course_id}")
                return {}
            
            attended, total = self.attendance[course_id]
            percentage = (attended / total * 100) if total > 0 else 0
            print(f"Course {course_id}: {attended}/{total} classes ({percentage:.1f}%)")
            return {course_id: self.attendance[course_id]}
        else:
            if not self.attendance:
                print("No attendance records available")
                return {}
            
            for c_id, (attended, total) in self.attendance.items():
                percentage = (attended / total * 100) if total > 0 else 0
                print(f"Course {c_id}: {attended}/{total} classes ({percentage:.1f}%)")
            return self.attendance
    
    def to_dict(self):
        """
        Convert student data to a dictionary for JSON serialization.
        
        Returns:
            dict: Student data as a dictionary
        """
        return {
            "name": self.name,
            "student_id": self.student_id,
            "level": self.level,
            "courses": self.courses,
            "grades": self.grades,
            "attendance": self.attendance
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Student instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing student data
            
        Returns:
            Student: A new Student instance
        """
        student = cls(data["name"], data["student_id"], data["level"])
        student.courses = data["courses"]
        student.grades = data["grades"]
        student.attendance = data["attendance"]
        return student
    
    def save_to_json(self, filename="data.json"):
        """
        Save student data to a JSON file.
        
        Args:
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            data = {}
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'r') as file:
                    data = json.load(file)
            
            if "students" not in data:
                data["students"] = {}
            
            data["students"][self.student_id] = self.to_dict()
            
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Student data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving student data: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, student_id, filename="data.json"):
        """
        Load student data from a JSON file.
        
        Args:
            student_id (str): ID of the student to load
            filename (str): Path to the JSON file
            
        Returns:
            Student: A Student instance if found, None otherwise
        """
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return None
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found in {filename}")
                return None
            
            student_data = data["students"][student_id]
            return cls.from_dict(student_data)
        except Exception as e:
            print(f"Error loading student data: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Create a new student
    student = Student("John Doe", "S12345", "Sophomore")
    
    # Register for courses
    student.register_course("CS101")
    student.register_course("MATH201")
    student.register_course("ENG105")
    
    # View registered courses
    student.view_courses()
    
    # Save to JSON
    student.save_to_json()
    
    # Load from JSON
    loaded_student = Student.load_from_json("S12345")
    if loaded_student:
        print(f"Loaded student: {loaded_student.name}")
        loaded_student.view_courses()

print("Student module loaded successfully")