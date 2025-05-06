"""
Main module for the University Management System.
Provides a simple command-line interface to interact with the system.
"""

import os
import json
from student import Student
from professor import Professor
from course import Course
from college import College
from registration import Registration
from attendance import Attendance
from grading import Grading

def initialize_data():
    """Initialize the data.json file with sample data if it doesn't exist."""
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        return
    
    # Create a college
    college = College("Tech University", "Silicon Valley")
    
    # Create students
    student1 = Student("John Doe", "S12345", "Sophomore")
    student2 = Student("Jane Smith", "S67890", "Freshman")
    
    # Create professors
    professor1 = Professor("Dr. Alan Turing", "P11111", "Computer Science")
    professor2 = Professor("Dr. Marie Curie", "P22222", "Physics")
    
    # Create courses
    course1 = Course("CS101", "Introduction to Computer Science", 30, 4)
    course2 = Course("PHYS201", "Physics I", 25, 4)
    course3 = Course("MATH201", "Calculus I", 25, 3)
    
    # Add entities to college
    college.add_student(student1)
    college.add_student(student2)
    college.add_professor(professor1)
    college.add_professor(professor2)
    college.add_course(course1)
    college.add_course(course2)
    college.add_course(course3)
    
    # Assign professors to courses
    college.assign_professor_to_course("P11111", "CS101")
    college.assign_professor_to_course("P22222", "PHYS201")
    
    # Register students for courses
    college.register_student_for_course("S12345", "CS101")
    college.register_student_for_course("S67890", "CS101")
    college.register_student_for_course("S12345", "PHYS201")
    
    # Save to JSON
    college.save_to_json()
    
    print("Sample data initialized successfully")

def display_menu():
    """Display the main menu."""
    print("\n===== University Management System =====")
    print("1. Student Management")
    print("2. Professor Management")
    print("3. Course Management")
    print("4. Registration Management")
    print("5. Attendance Management")
    print("6. Grading Management")
    print("7. College Management")
    print("0. Exit")
    print("=======================================")

def student_menu():
    """Display the student management menu."""
    print("\n===== Student Management =====")
    print("1. Add a new student")
    print("2. View student details")
    print("3. Update student information")
    print("4. Delete a student")
    print("5. View student's courses")
    print("6. View student's grades")
    print("7. Calculate student's GPA")
    print("8. View student's attendance")
    print("0. Back to main menu")
    print("============================")

def professor_menu():
    """Display the professor management menu."""
    print("\n===== Professor Management =====")
    print("1. Add a new professor")
    print("2. View professor details")
    print("3. Update professor information")
    print("4. Delete a professor")
    print("5. View professor's courses")
    print("6. Assign a course to a professor")
    print("7. Remove a course from a professor")
    print("0. Back to main menu")
    print("==============================")

def course_menu():
    """Display the course management menu."""
    print("\n===== Course Management =====")
    print("1. Add a new course")
    print("2. View course details")
    print("3. Update course information")
    print("4. Delete a course")
    print("5. View enrolled students")
    print("6. View course professor")
    print("0. Back to main menu")
    print("===========================")

def registration_menu():
    """Display the registration management menu."""
    print("\n===== Registration Management =====")
    print("1. Register a student for a course")
    print("2. Drop a course for a student")
    print("3. View registered courses for a student")
    print("4. View enrolled students in a course")
    print("0. Back to main menu")
    print("=================================")

def attendance_menu():
    """Display the attendance management menu."""
    print("\n===== Attendance Management =====")
    print("1. Mark attendance for a student")
    print("2. View attendance for a student")
    print("3. View attendance for a course")
    print("4. Generate attendance report")
    print("0. Back to main menu")
    print("===============================")

def grading_menu():
    """Display the grading management menu."""
    print("\n===== Grading Management =====")
    print("1. Assign a grade to a student")
    print("2. View grades for a student")
    print("3. View grades for a course")
    print("4. Calculate GPA for a student")
    print("5. View grade distribution for a course")
    print("0. Back to main menu")
    print("============================")

def college_menu():
    """Display the college management menu."""
    print("\n===== College Management =====")
    print("1. View college information")
    print("2. List all students")
    print("3. List all professors")
    print("4. List all courses")
    print("0. Back to main menu")
    print("===========================")

def handle_student_menu():
    """Handle the student management menu."""
    while True:
        student_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Add a new student
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            level = input("Enter student level (e.g., Freshman, Sophomore): ")
            
            student = Student(name, student_id, level)
            if student.save_to_json():
                print(f"Student {name} added successfully")
        
        elif choice == "2":
            # View student details
            student_id = input("Enter student ID: ")
            student = Student.load_from_json(student_id)
            
            if student:
                print(f"\nStudent Details:")
                print(f"Name: {student.name}")
                print(f"ID: {student.student_id}")
                print(f"Level: {student.level}")
                print(f"Courses: {', '.join(student.courses) if student.courses else 'None'}")
        
        elif choice == "3":
            # Update student information
            student_id = input("Enter student ID: ")
            student = Student.load_from_json(student_id)
            
            if student:
                print(f"\nCurrent Information:")
                print(f"Name: {student.name}")
                print(f"Level: {student.level}")
                
                name = input(f"Enter new name (or press Enter to keep '{student.name}'): ")
                level = input(f"Enter new level (or press Enter to keep '{student.level}'): ")
                
                if name:
                    student.name = name
                if level:
                    student.level = level
                
                if student.save_to_json():
                    print(f"Student information updated successfully")
        
        elif choice == "4":
            # Delete a student
            student_id = input("Enter student ID: ")
            
            try:
                # Load data from JSON
                if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
                    with open("data.json", 'r') as file:
                        data = json.load(file)
                    
                    if "students" in data and student_id in data["students"]:
                        # Remove student from courses
                        student_data = data["students"][student_id]
                        for course_id in student_data.get("courses", []):
                            if "courses" in data and course_id in data["courses"]:
                                if student_id in data["courses"][course_id]["enrolled_students"]:
                                    data["courses"][course_id]["enrolled_students"].remove(student_id)
                        
                        # Delete student
                        del data["students"][student_id]
                        
                        # Save updated data
                        with open("data.json", 'w') as file:
                            json.dump(data, file, indent=4)
                        
                        print(f"Student {student_id} deleted successfully")
                    else:
                        print(f"Student {student_id} not found")
                else:
                    print("No data found")
            except Exception as e:
                print(f"Error deleting student: {e}")
        
        elif choice == "5":
            # View student's courses
            student_id = input("Enter student ID: ")
            student = Student.load_from_json(student_id)
            
            if student:
                student.view_courses()
        
        elif choice == "6":
            # View student's grades
            student_id = input("Enter student ID: ")
            Grading.get_grade(student_id)
        
        elif choice == "7":
            # Calculate student's GPA
            student_id = input("Enter student ID: ")
            Grading.calculate_gpa(student_id)
        
        elif choice == "8":
            # View student's attendance
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID (or press Enter for all courses): ")
            
            if course_id:
                Attendance.get_attendance(student_id, course_id)
            else:
                Attendance.get_attendance(student_id)
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_professor_menu():
    """Handle the professor management menu."""
    while True:
        professor_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Add a new professor
            name = input("Enter professor name: ")
            professor_id = input("Enter professor ID: ")
            department = input("Enter professor department: ")
            
            professor = Professor(name, professor_id, department)
            if professor.save_to_json():
                print(f"Professor {name} added successfully")
        
        elif choice == "2":
            # View professor details
            professor_id = input("Enter professor ID: ")
            professor = Professor.load_from_json(professor_id)
            
            if professor:
                print(f"\nProfessor Details:")
                print(f"Name: {professor.name}")
                print(f"ID: {professor.professor_id}")
                print(f"Department: {professor.department}")
                print(f"Courses: {', '.join(professor.courses) if professor.courses else 'None'}")
        
        elif choice == "3":
            # Update professor information
            professor_id = input("Enter professor ID: ")
            professor = Professor.load_from_json(professor_id)
            
            if professor:
                print(f"\nCurrent Information:")
                print(f"Name: {professor.name}")
                print(f"Department: {professor.department}")
                
                name = input(f"Enter new name (or press Enter to keep '{professor.name}'): ")
                department = input(f"Enter new department (or press Enter to keep '{professor.department}'): ")
                
                if name:
                    professor.name = name
                if department:
                    professor.department = department
                
                if professor.save_to_json():
                    print(f"Professor information updated successfully")
        
        elif choice == "4":
            # Delete a professor
            professor_id = input("Enter professor ID: ")
            
            try:
                # Load data from JSON
                if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
                    with open("data.json", 'r') as file:
                        data = json.load(file)
                    
                    if "professors" in data and professor_id in data["professors"]:
                        # Remove professor from courses
                        professor_data = data["professors"][professor_id]
                        for course_id in professor_data.get("courses", []):
                            if "courses" in data and course_id in data["courses"]:
                                if data["courses"][course_id]["professor_id"] == professor_id:
                                    data["courses"][course_id]["professor_id"] = None
                        
                        # Delete professor
                        del data["professors"][professor_id]
                        
                        # Save updated data
                        with open("data.json", 'w') as file:
                            json.dump(data, file, indent=4)
                        
                        print(f"Professor {professor_id} deleted successfully")
                    else:
                        print(f"Professor {professor_id} not found")
                else:
                    print("No data found")
            except Exception as e:
                print(f"Error deleting professor: {e}")
        
        elif choice == "5":
            # View professor's courses
            professor_id = input("Enter professor ID: ")
            professor = Professor.load_from_json(professor_id)
            
            if professor:
                professor.view_courses()
        
        elif choice == "6":
            # Assign a course to a professor
            professor_id = input("Enter professor ID: ")
            course_id = input("Enter course ID: ")
            
            professor = Professor.load_from_json(professor_id)
            course = Course.load_from_json(course_id)
            
            if professor and course:
                if professor.assign_course(course_id) and course.assign_professor(professor_id):
                    professor.save_to_json()
                    course.save_to_json()
                    print(f"Course {course_id} assigned to professor {professor_id} successfully")
        
        elif choice == "7":
            # Remove a course from a professor
            professor_id = input("Enter professor ID: ")
            course_id = input("Enter course ID: ")
            
            professor = Professor.load_from_json(professor_id)
            course = Course.load_from_json(course_id)
            
            if professor and course:
                if professor.remove_course(course_id):
                    if course.professor_id == professor_id:
                        course.professor_id = None
                    
                    professor.save_to_json()
                    course.save_to_json()
                    print(f"Course {course_id} removed from professor {professor_id} successfully")
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_course_menu():
    """Handle the course management menu."""
    while True:
        course_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Add a new course
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            
            try:
                max_students = int(input("Enter maximum number of students: "))
                credits = int(input("Enter number of credits: "))
            except ValueError:
                print("Invalid input. Using default values.")
                max_students = 30
                credits = 3
            
            course = Course(course_id, course_name, max_students, credits)
            if course.save_to_json():
                print(f"Course {course_name} added successfully")
        
        elif choice == "2":
            # View course details
            course_id = input("Enter course ID: ")
            course = Course.load_from_json(course_id)
            
            if course:
                course.view_details()
        
        elif choice == "3":
            # Update course information
            course_id = input("Enter course ID: ")
            course = Course.load_from_json(course_id)
            
            if course:
                print(f"\nCurrent Information:")
                print(f"Name: {course.course_name}")
                print(f"Max Students: {course.max_students}")
                print(f"Credits: {course.credits}")
                
                course_name = input(f"Enter new name (or press Enter to keep '{course.course_name}'): ")
                
                try:
                    max_students_input = input(f"Enter new maximum number of students (or press Enter to keep {course.max_students}): ")
                    credits_input = input(f"Enter new number of credits (or press Enter to keep {course.credits}): ")
                    
                    max_students = int(max_students_input) if max_students_input else course.max_students
                    credits = int(credits_input) if credits_input else course.credits
                except ValueError:
                    print("Invalid input. Keeping original values.")
                    max_students = course.max_students
                    credits = course.credits
                
                if course_name:
                    course.course_name = course_name
                course.max_students = max_students
                course.credits = credits
                
                if course.save_to_json():
                    print(f"Course information updated successfully")
        
        elif choice == "4":
            # Delete a course
            course_id = input("Enter course ID: ")
            
            try:
                # Load data from JSON
                if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
                    with open("data.json", 'r') as file:
                        data = json.load(file)
                    
                    if "courses" in data and course_id in data["courses"]:
                        # Remove course from students
                        if "students" in data:
                            for student_id, student_data in data["students"].items():
                                if course_id in student_data.get("courses", []):
                                    student_data["courses"].remove(course_id)
                                    if "grades" in student_data and course_id in student_data["grades"]:
                                        del student_data["grades"][course_id]
                                    if "attendance" in student_data and course_id in student_data["attendance"]:
                                        del student_data["attendance"][course_id]
                        
                        # Remove course from professors
                        if "professors" in data:
                            for professor_id, professor_data in data["professors"].items():
                                if course_id in professor_data.get("courses", []):
                                    professor_data["courses"].remove(course_id)
                        
                        # Delete course
                        del data["courses"][course_id]
                        
                        # Save updated data
                        with open("data.json", 'w') as file:
                            json.dump(data, file, indent=4)
                        
                        print(f"Course {course_id} deleted successfully")
                    else:
                        print(f"Course {course_id} not found")
                else:
                    print("No data found")
            except Exception as e:
                print(f"Error deleting course: {e}")
        
        elif choice == "5":
            # View enrolled students
            course_id = input("Enter course ID: ")
            Registration.list_enrolled_students(course_id)
        
        elif choice == "6":
            # View course professor
            course_id = input("Enter course ID: ")
            course = Course.load_from_json(course_id)
            
            if course:
                if course.professor_id:
                    professor = Professor.load_from_json(course.professor_id)
                    if professor:
                        print(f"Professor for course {course_id}: {professor.name} ({professor.professor_id})")
                    else:
                        print(f"Professor {course.professor_id} not found")
                else:
                    print(f"No professor assigned to course {course_id}")
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_registration_menu():
    """Handle the registration management menu."""
    while True:
        registration_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Register a student for a course
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            
            Registration.register_student(student_id, course_id)
        
        elif choice == "2":
            # Drop a course for a student
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            
            Registration.drop_course(student_id, course_id)
        
        elif choice == "3":
            # View registered courses for a student
            student_id = input("Enter student ID: ")
            
            Registration.list_registered_courses(student_id)
        
        elif choice == "4":
            # View enrolled students in a course
            course_id = input("Enter course ID: ")
            
            Registration.list_enrolled_students(course_id)
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_attendance_menu():
    """Handle the attendance management menu."""
    while True:
        attendance_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Mark attendance for a student
            course_id = input("Enter course ID: ")
            student_id = input("Enter student ID: ")
            date = input("Enter date (YYYY-MM-DD): ")
            
            present_input = input("Was the student present? (y/n): ")
            present = present_input.lower() == 'y'
            
            Attendance.mark_attendance(course_id, student_id, present, date)
        
        elif choice == "2":
            # View attendance for a student
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID (or press Enter for all courses): ")
            
            if course_id:
                Attendance.get_attendance(student_id, course_id)
            else:
                Attendance.get_attendance(student_id)
        
        elif choice == "3":
            # View attendance for a course
            course_id = input("Enter course ID: ")
            
            Attendance.get_course_attendance(course_id)
        
        elif choice == "4":
            # Generate attendance report
            Attendance.get_attendance_report()
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_grading_menu():
    """Handle the grading management menu."""
    while True:
        grading_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Assign a grade to a student
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            grade = input("Enter grade (e.g., A, B+, C): ")
            
            Grading.assign_grade(student_id, course_id, grade)
        
        elif choice == "2":
            # View grades for a student
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID (or press Enter for all courses): ")
            
            if course_id:
                Grading.get_grade(student_id, course_id)
            else:
                Grading.get_grade(student_id)
        
        elif choice == "3":
            # View grades for a course
            course_id = input("Enter course ID: ")
            
            Grading.get_course_grades(course_id)
        
        elif choice == "4":
            # Calculate GPA for a student
            student_id = input("Enter student ID: ")
            
            Grading.calculate_gpa(student_id)
        
        elif choice == "5":
            # View grade distribution for a course
            course_id = input("Enter course ID: ")
            
            Grading.get_grade_distribution(course_id)
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def handle_college_menu():
    """Handle the college management menu."""
    while True:
        college_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # View college information
            college = College.load_from_json()
            
            if college:
                print(f"\nCollege Information:")
                print(f"Name: {college.name}")
                print(f"Location: {college.location}")
                print(f"Number of Students: {len(college.students)}")
                print(f"Number of Professors: {len(college.professors)}")
                print(f"Number of Courses: {len(college.courses)}")
        
        elif choice == "2":
            # List all students
            college = College.load_from_json()
            
            if college:
                college.list_students()
        
        elif choice == "3":
            # List all professors
            college = College.load_from_json()
            
            if college:
                college.list_professors()
        
        elif choice == "4":
            # List all courses
            college = College.load_from_json()
            
            if college:
                college.list_courses()
        
        elif choice == "0":
            # Back to main menu
            break
        
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function to run the University Management System."""
    initialize_data()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            handle_student_menu()
        elif choice == "2":
            handle_professor_menu()
        elif choice == "3":
            handle_course_menu()
        elif choice == "4":
            handle_registration_menu()
        elif choice == "5":
            handle_attendance_menu()
        elif choice == "6":
            handle_grading_menu()
        elif choice == "7":
            handle_college_menu()
        elif choice == "0":
            print("Thank you for using the University Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

print("Main module loaded successfully")