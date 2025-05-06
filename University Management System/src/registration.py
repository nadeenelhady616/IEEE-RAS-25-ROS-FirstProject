from student_system import Student
from course import Course
from department import Department
from college import College
import json
def register_student(filename, college):
    """
    Function to register a new student.
    """
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    level = int(input("Enter level: "))
    department = input("Enter department: ")

    student = Student(student_id, name, level, department)
    college.add_student(student)
    with open(filename, 'r') as file:
        data = json.load(file)
    if student_id in data['students']:
        print(f"Student with ID {student_id} already exists.")
        return
    else:
        data['students'][student_id] = {
            'name': name,
            'level': level,
            'department': department
        }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Student {name} registered successfully.")
    
def register_course(filename, student, course):
    """
    Function to register a course for a student.
    """
    with open(filename, 'r') as file:
        data = json.load(file) 
    if student.student_id not in data['students']:
        print(f"Student with ID {student.student_id} not found.")
        return
    if course.course_id in student.courses_reg:
        print(f"Already registered for {course.course_name}.")
        return
    if student.level < course.level:
        print(f"Course {course.course_name} is not available for your level.")
        return
    student.register_course(course)
    data['students'][student.student_id]['courses'].append(course.course_id)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Registered for {course.course_name} successfully.")

def drop_course(filename, student, course):
    """
    Function to drop a course for a student.
    """
    with open(filename, 'r') as file:
        data = json.load(file)      
    if student.student_id not in data['students']:
        print(f"Student with ID {student.student_id} not found.")
        return
    if course.course_id not in student.courses_reg:
        print(f"Not registered for {course.course_name}.")
        return
    student.drop_course(course)
    data['students'][student.student_id]['courses'].remove(course.course_id)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Dropped {course.course_name} successfully.")


