# student_system.py
class Student:
    def __init__(self, name, student_id, level, department):
        self.student_id = student_id
        self.name = name
        self.level = level
        self.department = department
        self.courses_reg = []
        self.grades = {}  # {course_id: grade}
        self.attendance = {}  # {course_id: {date: status}}

    def register_course(self, course):
        if course not in self.courses_reg:
            self.courses_reg.append(course)
            course.add_student(self.student_id, self.name, self.level, self.department)
            self.grades[course.course_id] = 0
            self.attendance[course.course_id] = {}
            print(f"Registered for {course.course_name}")
            return True
        print(f"Already registered for {course.course_name}")
        return False
    
    def drop_course(self, course):
        if course in self.courses_reg:
            self.courses_reg.remove(course)
            course.remove_student(self.student_id)
            print(f"Dropped {course.course_name}")
            return True
        print(f"Not registered for {course.course_name}")
        return False
    
    def calculate_gpa(self):
        if not self.grades:
            print("No grades available")
            return 0.0
        
        total = sum(self.grades.values())
        count = len(self.grades)
        gpa = total / count if count > 0 else 0
        print(f"GPA: {gpa:.2f}")
        return gpa
    
    def print_student_info(self):
        print(f"\nStudent: {self.name} (ID: {self.student_id})")
        print(f"Level: {self.level}, Department: {self.department}")
        print(f"Courses: {len(self.courses_reg)}")
        print(f"GPA: {self.calculate_gpa():.2f}")
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "level": self.level,
            "department": self.department,
            "courses_reg": [course.course_id for course in self.courses_reg],
            "grades": self.grades,
            "attendance": self.attendance
        }
    def from_dict(data):
        student = Student(data['name'], data['student_id'], data['level'], data['department'])
        student.courses_reg = data['courses_reg']
        student.grades = data['grades']
        student.attendance = data['attendance']
        return student

def student_menu(student, available_courses):
    while True:
        print("\n====== Student Menu ======")
        print("1. View My Information")
        print("2. Register for a Course")
        print("3. Drop a Course")
        print("4. Calculate GPA")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            student.print_student_info()
            
            if student.courses:
                print("\nRegistered Courses:")
                for i, course in enumerate(student.courses, 1):
                    print(f"{i}. {course.course_name}")
                    grade = student.grades.get(course.course_id, 0)
                    print(f"   Grade: {grade}")

        elif choice == '2':
            print("\nAvailable Courses:")
            for i, course in enumerate(available_courses, 1):
                print(f"{i}. {course.course_name}")
            
            try:
                index = int(input("Enter course number: ")) - 1
                if 0 <= index < len(available_courses):
                    student.register_course(available_courses[index])
                else:
                    print("Invalid course number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '3':
            if not student.courses:
                print("Not registered for any courses.")
                continue
                
            print("\nRegistered Courses:")
            for i, course in enumerate(student.courses, 1):
                print(f"{i}. {course.course_name}")
            
            try:
                index = int(input("Enter course number to drop: ")) - 1
                if 0 <= index < len(student.courses):
                    student.drop_course(student.courses[index])
                else:
                    print("Invalid course number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            student.calculate_gpa()

        elif choice == '5':
            print("Exiting student menu.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    from course import Course
    
    # Sample data
    c1 = Course("CS101", "Intro to CS", "CS", 1, "Engineering")
    c2 = Course("MATH101", "Calculus I", "MATH", 1, "Science")
    
    s1 = Student("S001", "Ali", 1, "Engineering")
    s1.register_course(c1)
    
    student_menu(s1, [c1, c2])