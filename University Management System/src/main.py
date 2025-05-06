import json
from college import College
from student_system import Student
from course import Course
from department import Department
from registration import register_student, register_course, drop_course
from attendance import Attendance
from grading_system import Grading
from professor import Professor
import config

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)

def initialize_data():
    # Create a college
    college = College("Tech University")
    
    # Create students
    student1 = Student("John Doe", "S12345", "1e", "Computer Science")
    student2 = Student("Jane Smith", "S67890", "2", "electrical Engineering")
    
    # Create professors
    professor1 = Professor("Dr. Alan Turing", "P11111", "Computer Science")
    professor2 = Professor("Dr. Marie Curie", "P22222", "Physics")
    
    # Create departments
    department1 = Department("Computer Science")
    department2 = Department("electrical Engineering")

    # Create courses
    course1 = Course("CS101", "Introduction to Computer Science", 3, 1)
    course2 = Course("PHYS201", "Physics I", 3, 2)
    course3 = Course("MATH201", "Calculus I", 3, 1)
    
    # Add courses to departments
    department1.add_course(course1)
    department1.add_course(course3)
    department2.add_course(course2)

    # Add entities to college
    college.add_student(student1)
    college.add_student(student2)
    college.add_professor(professor1)
    college.add_professor(professor2)
    college.add_department(department1)
    college.add_department(department2)
    
    # Assign professors to courses
    course1.assign_professor(professor1)
    course2.assign_professor(professor2)
    
    # Serialize data
    data = {
        "college": college.to_dict(),
        "students": [student1.to_dict(), student2.to_dict()],
        "professors": [professor1.to_dict(), professor2.to_dict()],
        "departments": [department1.to_dict(), department2.to_dict()],
        "courses": [course1.to_dict(), course2.to_dict(), course3.to_dict()]
    }

    print("Sample data initialized successfully")
    return data

def display_menu():
    """Display the main menu."""
    print("\n===== University Management System =====")
    print("1. Student")
    print("2. Professor")
    print("3. Admin")
    print("0. Exit")
    print("=======================================")
    choice = input("Enter your choice (0-3): ")
    return choice


def student_menu(student, filename):
    while True:
        print("\n====== Student Menu ======")
        print("1. View My Information")
        print("2. Register for a Course")
        print("3. Drop a Course")
        print("4. Calculate GPA")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            print("\n--- My Information ---")
            print(json.dumps(student.to_dict(), indent=4))
        elif choice == "2":
            course_id = input("Enter the Course ID to register: ")
            register_student(student, course_id, filename)
        elif choice == "3":
            course_id = input("Enter the Course ID to drop: ")
            drop_course(student, course_id, filename)
        elif choice == "4":
            gpa = student.calculate_gpa()
            print(f"\nYour GPA is: {gpa:.2f}")
        elif choice == "5":
            print("Exiting Student Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def professor_menu(professor, filename):
                while True:
                    print("\n====== Professor Menu ======")
                    print("1. View My Information")
                    print("2. View Assigned Courses")
                    print("3. Record Attendance")
                    print("4. Assign Grades")
                    print("5. Exit")

                    choice = input("Enter your choice (1-5): ")
                    if choice == "1":
                        print("\n--- My Information ---")
                        print(json.dumps(professor.to_dict(), indent=4))
                    elif choice == "2":
                        print("\n--- Assigned Courses ---")
                        for course in professor.get_assigned_courses():
                            print(f"Course ID: {course.course_code}, Name: {course.name}")
                    elif choice == "3":
                        course_id = input("Enter the Course ID to record attendance: ")
                        student_id = input("Enter the Student ID: ")
                        status = input("Enter Attendance Status (Present/Absent): ")
                        Attendance.record_attendance(course_id, student_id, status, filename)
                        print("Attendance recorded successfully.")
                    elif choice == "4":
                        course_id = input("Enter the Course ID to assign grades: ")
                        student_id = input("Enter the Student ID: ")
                        grade = input("Enter Grade: ")
                        Grading.assign_grade(course_id, student_id, grade, filename)
                        print("Grade assigned successfully.")
                    elif choice == "5":
                        print("Exiting Professor Menu...")
                        break
                    else:
                        print("Invalid choice. Please try again.")

def admin_menu(college):
    while True:
        print("\n====== Admin Menu ======")
        print("1. View College Information")
        print("2. Add Student")
        print("3. Add Professor")
        print("4. Add Course")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            print("\n--- College Information ---")
            print(json.dumps(college.to_dict(), indent=4))
        elif choice == "2":
            student_id = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            level = input("Enter Student Level: ")
            department = input("Enter Student Department: ")
            college.add_student(Student(name, student_id, level, department))
            print(f"Student {name} added successfully.")
        elif choice == "3":
            professor_id = input("Enter Professor ID: ")
            name = input("Enter Professor Name: ")
            department = input("Enter Professor Department: ")
            college.add_professor(Professor(name, professor_id, department))
            print(f"Professor {name} added successfully.")
        elif choice == "4":
            course_id = input("Enter Course ID: ")
            name = input("Enter Course Name: ")
            credits = int(input("Enter Course Credits: "))
            level = int(input("Enter Course Level: "))
            department_name = input("Enter Department Name: ")

            # Create a new course
            new_course = Course(course_id, name, credits, level)

            # Find the department and add the course
            department = college.get_department(department_name)
            if department:
                department.add_course(new_course)
                print(f"Course {name} added to department {department_name} successfully.")
            else:
                print(f"Department {department_name} not found.")
            print(f"Course {name} added successfully.")
        elif choice == "5":
            print("Exiting Admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    c = initialize_data()
    with open("college_data.json", "w") as json_file:
        json.dump(c, json_file, indent=4, cls=CustomEncoder)
    print("Data saved to college_data.json")
    
    while True:
        choice = display_menu()
        if choice == "1":
            student_id = input("Enter your Student ID: ")
            with open("college_data.json", "r") as json_file:
                data = json.load(json_file)
            student_data = next((s for s in data["students"] if s["student_id"] == student_id), None)
            if student_data:
                student = Student.from_dict(student_data)
                student_menu(student, "college_data.json")
            else:
                print("Student not found.")
        elif choice == "2":
            professor_id = input("Enter your Professor ID: ")
            with open("college_data.json", "r") as json_file:
                data = json.load(json_file)
            professor_data = next((p for p in data["professors"] if p["professor_id"] == professor_id), None)
            if professor_data:
                professor = Professor.from_dict(professor_data)
                professor_menu(professor, "college_data.json")
            else:
                print("Professor not found.")
        elif choice == "3":
            with open("college_data.json", "r") as json_file:
                data = json.load(json_file)
            college = College.from_dict(data["college"])
            admin_menu(college)
        elif choice == "0":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    


        
