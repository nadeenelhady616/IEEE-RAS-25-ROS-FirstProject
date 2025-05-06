"""
Course module for the University Management System.
Handles course data and operations.
"""

import json
import os

class Course:
    """
    Represents a course in the university system.
    """
    
    def __init__(self, course_id, course_name, max_students, credits=3):
        """
        Initialize a new Course instance.
        
        Args:
            course_id (str): Unique identifier for the course
            course_name (str): The name of the course
            max_students (int): Maximum number of students allowed in the course
            credits (int, optional): Number of credits for the course
        """
        self.course_id = course_id
        self.course_name = course_name
        self.max_students = max_students
        self.credits = credits
        self.professor_id = None
        self.enrolled_students = []
    
    def assign_professor(self, professor_id):
        """
        Assign a professor to teach this course.
        
        Args:
            professor_id (str): The ID of the professor to assign
            
        Returns:
            bool: True if assignment was successful, False otherwise
        """
        self.professor_id = professor_id
        print(f"Professor {professor_id} assigned to course {self.course_id}")
        return True
    
    def enroll_student(self, student_id):
        """
        Enroll a student in this course.
        
        Args:
            student_id (str): The ID of the student to enroll
            
        Returns:
            bool: True if enrollment was successful, False otherwise
        """
        if len(self.enrolled_students) >= self.max_students:
            print(f"Course {self.course_id} is full")
            return False
        
        if student_id in self.enrolled_students:
            print(f"Student {student_id} is already enrolled in course {self.course_id}")
            return False
        
        self.enrolled_students.append(student_id)
        print(f"Student {student_id} enrolled in course {self.course_id}")
        return True
    
    def drop_student(self, student_id):
        """
        Drop a student from this course.
        
        Args:
            student_id (str): The ID of the student to drop
            
        Returns:
            bool: True if the student was dropped, False otherwise
        """
        if student_id not in self.enrolled_students:
            print(f"Student {student_id} is not enrolled in course {self.course_id}")
            return False
        
        self.enrolled_students.remove(student_id)
        print(f"Student {student_id} dropped from course {self.course_id}")
        return True
    
    def get_enrollment_count(self):
        """
        Get the current number of students enrolled in the course.
        
        Returns:
            int: Number of enrolled students
        """
        return len(self.enrolled_students)
    
    def is_full(self):
        """
        Check if the course is at maximum capacity.
        
        Returns:
            bool: True if the course is full, False otherwise
        """
        return len(self.enrolled_students) >= self.max_students
    
    def view_details(self):
        """
        View details of the course.
        
        Returns:
            dict: Course details
        """
        details = {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "professor_id": self.professor_id,
            "credits": self.credits,
            "enrollment": f"{len(self.enrolled_students)}/{self.max_students}"
        }
        
        print(f"Course: {self.course_name} ({self.course_id})")
        print(f"Professor: {self.professor_id or 'Not assigned'}")
        print(f"Credits: {self.credits}")
        print(f"Enrollment: {len(self.enrolled_students)}/{self.max_students}")
        
        return details
    
    def to_dict(self):
        """
        Convert course data to a dictionary for JSON serialization.
        
        Returns:
            dict: Course data as a dictionary
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "max_students": self.max_students,
            "credits": self.credits,
            "professor_id": self.professor_id,
            "enrolled_students": self.enrolled_students
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Course instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing course data
            
        Returns:
            Course: A new Course instance
        """
        course = cls(
            data["course_id"],
            data["course_name"],
            data["max_students"],
            data["credits"]
        )
        course.professor_id = data["professor_id"]
        course.enrolled_students = data["enrolled_students"]
        return course
    
    def save_to_json(self, filename="data.json"):
        """
        Save course data to a JSON file.
        
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
            
            if "courses" not in data:
                data["courses"] = {}
            
            data["courses"][self.course_id] = self.to_dict()
            
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Course data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving course data: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, course_id, filename="data.json"):
        """
        Load course data from a JSON file.
        
        Args:
            course_id (str): ID of the course to load
            filename (str): Path to the JSON file
            
        Returns:
            Course: A Course instance if found, None otherwise
        """
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return None
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found in {filename}")
                return None
            
            course_data = data["courses"][course_id]
            return cls.from_dict(course_data)
        except Exception as e:
            print(f"Error loading course data: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Create a new course
    course = Course("CS101", "Introduction to Computer Science", 30, 4)
    
    # Assign a professor
    course.assign_professor("P54321")
    
    # Enroll students
    course.enroll_student("S12345")
    course.enroll_student("S67890")
    
    # View course details
    course.view_details()
    
    # Save to JSON
    course.save_to_json()
    
    # Load from JSON
    loaded_course = Course.load_from_json("CS101")
    if loaded_course:
        print(f"Loaded course: {loaded_course.course_name}")
        loaded_course.view_details()

print("Course module loaded successfully")