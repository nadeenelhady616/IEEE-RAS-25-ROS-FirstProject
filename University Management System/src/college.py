"""
College module for the University Management System.
Handles college-wide operations and coordination.
"""

import json
import os
from student import Student
from professor import Professor
from course import Course

class College:
    """
    Represents a college in the university system.
    Manages students, professors, and courses.
    """
    
    def __init__(self, name, location):
        """
        Initialize a new College instance.
        
        Args:
            name (str): The name of the college
            location (str): The location of the college
        """
        self.name = name
        self.location = location
        self.students = {}  # student_id: Student
        self.professors = {}  # professor_id: Professor
        self.courses = {}  # course_id: Course
    
    def add_student(self, student):
        """
        Add a student to the college.
        
        Args:
            student (Student): The student to add
            
        Returns:
            bool: True if the student was added, False otherwise
        """
        if student.student_id in self.students:
            print(f"Student with ID {student.student_id} already exists")
            return False
        
        self.students[student.student_id] = student
        print(f"Student {student.name} added to {self.name}")
        return True
    
    def add_professor(self, professor):
        """
        Add a professor to the college.
        
        Args:
            professor (Professor): The professor to add
            
        Returns:
            bool: True if the professor was added, False otherwise
        """
        if professor.professor_id in self.professors:
            print(f"Professor with ID {professor.professor_id} already exists")
            return False
        
        self.professors[professor.professor_id] = professor
        print(f"Professor {professor.name} added to {self.name}")
        return True
    
    def add_course(self, course):
        """
        Add a course to the college.
        
        Args:
            course (Course): The course to add
            
        Returns:
            bool: True if the course was added, False otherwise
        """
        if course.course_id in self.courses:
            print(f"Course with ID {course.course_id} already exists")
            return False
        
        self.courses[course.course_id] = course
        print(f"Course {course.course_name} added to {self.name}")
        return True
    
    def get_student(self, student_id):
        """
        Get a student by ID.
        
        Args:
            student_id (str): The ID of the student to get
            
        Returns:
            Student: The student if found, None otherwise
        """
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found")
            return None
        
        return self.students[student_id]
    
    def get_professor(self, professor_id):
        """
        Get a professor by ID.
        
        Args:
            professor_id (str): The ID of the professor to get
            
        Returns:
            Professor: The professor if found, None otherwise
        """
        if professor_id not in self.professors:
            print(f"Professor with ID {professor_id} not found")
            return None
        
        return self.professors[professor_id]
    
    def get_course(self, course_id):
        """
        Get a course by ID.
        
        Args:
            course_id (str): The ID of the course to get
            
        Returns:
            Course: The course if found, None otherwise
        """
        if course_id not in self.courses:
            print(f"Course with ID {course_id} not found")
            return None
        
        return self.courses[course_id]
    
    def list_students(self):
        """
        List all students in the college.
        
        Returns:
            dict: Dictionary of student IDs to Student objects
        """
        if not self.students:
            print("No students enrolled in the college")
        else:
            print(f"Students enrolled in {self.name}:")
            for student_id, student in self.students.items():
                print(f"  {student_id}: {student.name} ({student.level})")
        
        return self.students
    
    def list_professors(self):
        """
        List all professors in the college.
        
        Returns:
            dict: Dictionary of professor IDs to Professor objects
        """
        if not self.professors:
            print("No professors employed by the college")
        else:
            print(f"Professors employed by {self.name}:")
            for professor_id, professor in self.professors.items():
                print(f"  {professor_id}: {professor.name} ({professor.department})")
        
        return self.professors
    
    def list_courses(self):
        """
        List all courses in the college.
        
        Returns:
            dict: Dictionary of course IDs to Course objects
        """
        if not self.courses:
            print("No courses offered by the college")
        else:
            print(f"Courses offered by {self.name}:")
            for course_id, course in self.courses.items():
                print(f"  {course_id}: {course.course_name} (Enrollment: {course.get_enrollment_count()}/{course.max_students})")
        
        return self.courses
    
    def register_student_for_course(self, student_id, course_id):
        """
        Register a student for a course.
        
        Args:
            student_id (str): The ID of the student
            course_id (str): The ID of the course
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        student = self.get_student(student_id)
        if not student:
            return False
        
        course = self.get_course(course_id)
        if not course:
            return False
        
        if course.is_full():
            print(f"Course {course_id} is full")
            return False
        
        # Register student in course
        if student.register_course(course_id) and course.enroll_student(student_id):
            print(f"Student {student.name} registered for course {course.course_name}")
            return True
        
        return False
    
    def assign_professor_to_course(self, professor_id, course_id):
        """
        Assign a professor to teach a course.
        
        Args:
            professor_id (str): The ID of the professor
            course_id (str): The ID of the course
            
        Returns:
            bool: True if assignment was successful, False otherwise
        """
        professor = self.get_professor(professor_id)
        if not professor:
            return False
        
        course = self.get_course(course_id)
        if not course:
            return False
        
        # Assign professor to course
        if professor.assign_course(course_id) and course.assign_professor(professor_id):
            print(f"Professor {professor.name} assigned to teach {course.course_name}")
            return True
        
        return False
    
    def to_dict(self):
        """
        Convert college data to a dictionary for JSON serialization.
        
        Returns:
            dict: College data as a dictionary
        """
        return {
            "name": self.name,
            "location": self.location
        }
    
    def save_to_json(self, filename="data.json"):
        """
        Save college data to a JSON file.
        
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
            
            # Save college info
            data["college"] = self.to_dict()
            
            # Save all students, professors, and courses
            for student_id, student in self.students.items():
                if "students" not in data:
                    data["students"] = {}
                data["students"][student_id] = student.to_dict()
            
            for professor_id, professor in self.professors.items():
                if "professors" not in data:
                    data["professors"] = {}
                data["professors"][professor_id] = professor.to_dict()
            
            for course_id, course in self.courses.items():
                if "courses" not in data:
                    data["courses"] = {}
                data["courses"][course_id] = course.to_dict()
            
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"College data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving college data: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, filename="data.json"):
        """
        Load college data from a JSON file.
        
        Args:
            filename (str): Path to the JSON file
            
        Returns:
            College: A College instance if found, None otherwise
        """
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return None
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "college" not in data:
                print(f"College data not found in {filename}")
                return None
            
            college_data = data["college"]
            college = cls(college_data["name"], college_data["location"])
            
            # Load students
            if "students" in data:
                for student_id, student_data in data["students"].items():
                    student = Student.from_dict(student_data)
                    college.students[student_id] = student
            
            # Load professors
            if "professors" in data:
                for professor_id, professor_data in data["professors"].items():
                    professor = Professor.from_dict(professor_data)
                    college.professors[professor_id] = professor
            
            # Load courses
            if "courses" in data:
                for course_id, course_data in data["courses"].items():
                    course = Course.from_dict(course_data)
                    college.courses[course_id] = course
            
            print(f"College data loaded from {filename}")
            return college
        except Exception as e:
            print(f"Error loading college data: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Create a new college
    college = College("Tech University", "Silicon Valley")
    
    # Create and add students
    student1 = Student("John Doe", "S12345", "Sophomore")
    student2 = Student("Jane Smith", "S67890", "Freshman")
    college.add_student(student1)
    college.add_student(student2)
    
    # Create and add professors
    professor1 = Professor("Dr. Alan Turing", "P11111", "Computer Science")
    professor2 = Professor("Dr. Marie Curie", "P22222", "Physics")
    college.add_professor(professor1)
    college.add_professor(professor2)
    
    # Create and add courses
    course1 = Course("CS101", "Introduction to Computer Science", 30, 4)
    course2 = Course("PHYS201", "Physics I", 25, 4)
    college.add_course(course1)
    college.add_course(course2)
    
    # Assign professors to courses
    college.assign_professor_to_course("P11111", "CS101")
    college.assign_professor_to_course("P22222", "PHYS201")
    
    # Register students for courses
    college.register_student_for_course("S12345", "CS101")
    college.register_student_for_course("S67890", "CS101")
    college.register_student_for_course("S12345", "PHYS201")
    
    # List all entities
    college.list_students()
    college.list_professors()
    college.list_courses()
    
    # Save to JSON
    college.save_to_json()
    
    # Load from JSON
    loaded_college = College.load_from_json()
    if loaded_college:
        print(f"Loaded college: {loaded_college.name}")
        loaded_college.list_students()

print("College module loaded successfully")