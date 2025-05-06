# grading_system.py
from student_system import Student
from course import Course
class Grading:
    def assign_grade(student, course, grade):
        if course.course_id in student.grades:
            student.grades[course.course_id] = grade
            print(f"Grade {grade} assigned to {student.name}")
            return True
        print(f"Student not registered for {course.course_name}")
        return False
    
    def view_student_grades(student):
        if not student.grades:
            print("No grades available")
            return
        
        print(f"\nGrades for {student.name}:")
        for course in student.courses_reg:
            grade = student.grades.get(course.course_id, 0)
            print(f"{course.course_name}: {grade}")
  



def grading_menu(students, courses):
    while True:
        print("\n====== Grading Menu ======")
        print("1. Assign Grade")
        print("2. View Student Grades")
        print("3. View Course Grades")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':

            print("\nStudents:")
            for i, student in enumerate(students, 1):
                print(f"{i}. {student.name}")
            
            try:
                s_index = int(input("Select student: ")) - 1
                if not (0 <= s_index < len(students)):
                    print("Invalid student number.")
                    continue
                
                student = students[s_index]
                
                if not student.courses:
                    print("Student not registered for any courses.")
                    continue
                
                print("\nCourses:")
                for i, course in enumerate(student.courses, 1):
                    print(f"{i}. {course.course_name}")
                
                c_index = int(input("Select course: ")) - 1
                if not (0 <= c_index < len(student.courses)):
                    print("Invalid course number.")
                    continue
                
                course = student.courses[c_index]
                
                try:
                    grade = float(input("Enter grade: "))
                    Grading.assign_grade(student, course, grade)
                except ValueError:
                    print("Please enter a valid grade.")
            
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '2':
            # Select student
            print("\nStudents:")
            for i, student in enumerate(students, 1):
                print(f"{i}. {student.name}")
            
            try:
                index = int(input("Select student: ")) - 1
                if 0 <= index < len(students):
                    Grading.view_student_grades(students[index])
                else:
                    print("Invalid student number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '3':
            # Select course
            print("\nCourses:")
            for i, course in enumerate(courses, 1):
                print(f"{i}. {course.course_name}")
            
            try:
                index = int(input("Select course: ")) - 1
                if 0 <= index < len(courses):
                    Grading.view_course_grades(courses[index])
                else:
                    print("Invalid course number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            print("Exiting grading menu.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    from course import Course
    from student_system import Student
    
    c1 = Course("CS101", "Intro to CS", "CS", 1, "Engineering")
    
    s1 = Student("S001", "Ali", 1, "Engineering")
    s1.register_course(c1)
    
    Grading.assign_grade(s1, c1, 85)
    
    grading_menu([s1], [c1])