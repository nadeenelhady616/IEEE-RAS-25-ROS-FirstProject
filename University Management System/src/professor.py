"""
Professor module for the University Management System.
Handles professor data and operations.
"""

import json
import os

class Professor:
    """
    Represents a professor in the university system.
    """
    
    def __init__(self, name, professor_id, department):
        """
        Initialize a new Professor instance.
        
        Args:
            name (str): The professor's full name
            professor_id (str): Unique identifier for the professor
            department (str): The department the professor belongs to
        """
        self.name = name
        self.professor_id = professor_id
        self.department = department
        self.courses = []  # List of course IDs the professor teaches
    
    def assign_course(self, course_id):
        """
        Assign a course to the professor.
        
        Args:
            course_id (str): The ID of the course to assign
            
        Returns:
            bool: True if assignment was successful, False otherwise
        """
        if course_id in self.courses:
            print(f"Already teaching course {course_id}")
            return False
        
        self.courses.append(course_id)
        print(f"Successfully assigned to teach course {course_id}")
        return True
    
    def remove_course(self, course_id):
        """
        Remove a course from the professor's teaching load.
        
        Args:
            course_id (str): The ID of the course to remove
            
        Returns:
            bool: True if the course was removed, False otherwise
        """
        if course_id not in self.courses:
            print(f"Not teaching course {course_id}")
            return False
        
        self.courses.remove(course_id)
        print(f"Successfully removed from teaching course {course_id}")
        return True
    
    def view_courses(self):
        """
        View all courses the professor is teaching.
        
        Returns:
            list: List of course IDs
        """
        if not self.courses:
            print("Not teaching any courses")
        else:
            print(f"Teaching courses: {', '.join(self.courses)}")
        return self.courses
    
    def grade_student(self, student_id, course_id, grade, filename="data.json"):
        """
        Assign a grade to a student for a specific course.
        
        Args:
            student_id (str): The ID of the student to grade
            course_id (str): The ID of the course
            grade (str): The grade to assign (e.g., 'A', 'B+')
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if grading was successful, False otherwise
        """
        if course_id not in self.courses:
            print(f"Not authorized to grade for course {course_id}")
            return False
        
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return False
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return False
            
            # Check if student is enrolled in the course
            student_data = data["students"][student_id]
            if course_id not in student_data["courses"]:
                print(f"Student {student_id} is not enrolled in course {course_id}")
                return False
            
            # Assign grade
            student_data["grades"][course_id] = grade
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Successfully assigned grade {grade} to student {student_id} for course {course_id}")
            return True
        except Exception as e:
            print(f"Error grading student: {e}")
            return False
    
    def mark_attendance(self, course_id, student_id, present, filename="data.json"):
        """
        Mark attendance for a student in a specific course.
        
        Args:
            course_id (str): The ID of the course
            student_id (str): The ID of the student
            present (bool): Whether the student was present
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if attendance marking was successful, False otherwise
        """
        if course_id not in self.courses:
            print(f"Not authorized to mark attendance for course {course_id}")
            return False
        
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return False
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return False
            
            # Check if student is enrolled in the course
            student_data = data["students"][student_id]
            if course_id not in student_data["courses"]:
                print(f"Student {student_id} is not enrolled in course {course_id}")
                return False
            
            # Update attendance
            if course_id not in student_data["attendance"]:
                student_data["attendance"][course_id] = [0, 0]
            
            student_data["attendance"][course_id][1] += 1  # Increment total classes
            if present:
                student_data["attendance"][course_id][0] += 1  # Increment attended classes
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            status = "present" if present else "absent"
            print(f"Marked student {student_id} as {status} for course {course_id}")
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
    
    def to_dict(self):
        """
        Convert professor data to a dictionary for JSON serialization.
        
        Returns:
            dict: Professor data as a dictionary
        """
        return {
            "name": self.name,
            "professor_id": self.professor_id,
            "department": self.department,
            "courses": self.courses
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Professor instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing professor data
            
        Returns:
            Professor: A new Professor instance
        """
        professor = cls(data["name"], data["professor_id"], data["department"])
        professor.courses = data["courses"]
        return professor
    
    def save_to_json(self, filename="data.json"):
        """
        Save professor data to a JSON file.
        
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
            
            if "professors" not in data:
                data["professors"] = {}
            
            data["professors"][self.professor_id] = self.to_dict()
            
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Professor data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving professor data: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, professor_id, filename="data.json"):
        """
        Load professor data from a JSON file.
        
        Args:
            professor_id (str): ID of the professor to load
            filename (str): Path to the JSON file
            
        Returns:
            Professor: A Professor instance if found, None otherwise
        """
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return None
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "professors" not in data or professor_id not in data["professors"]:
                print(f"Professor {professor_id} not found in {filename}")
                return None
            
            professor_data = data["professors"][professor_id]
            return cls.from_dict(professor_data)
        except Exception as e:
            print(f"Error loading professor data: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Create a new professor
    professor = Professor("Dr. Jane Smith", "P54321", "Computer Science")
    
    # Assign courses
    professor.assign_course("CS101")
    professor.assign_course("CS202")
    
    # View assigned courses
    professor.view_courses()
    
    # Save to JSON
    professor.save_to_json()
    
    # Load from JSON
    loaded_professor = Professor.load_from_json("P54321")
    if loaded_professor:
        print(f"Loaded professor: {loaded_professor.name}")
        loaded_professor.view_courses()

print("Professor module loaded successfully")