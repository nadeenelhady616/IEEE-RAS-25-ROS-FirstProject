from student_system import Student
from department import Department
from professor import Professor
class College:
    def __init__(self, name):
        self.name = name
        self.departments = {}
        self.students = {}
        self.professors = {}
    
    def add_department(self, department):
        if department.name not in self.departments:
            self.departments[department.name] = department
        else:
            print(f"Department {department.name} already exists.")
    
    def add_professor(self, professor):
        if professor.professor_id in self.professors:
            print(f"Professor with ID {professor.professor_id} already exists")
            return False
        
        self.professors[professor.professor_id] = professor
        print(f"Professor {professor.name} added to {self.name}")
        return True
    

    def add_student(self, student):
        if student.student_id in self.students:
            print(f"Student with ID {student.student_id} already exists")
            return False
        
        self.students[student.student_id] = student
        print(f"Student {student.name} added to {self.name}")
        return True
    
    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print(f"Student with ID {student_id} removed from {self.name}")
            return True
        else:
            print(f"Student with ID {student_id} not found")
            return False
        
    def get_student(self, student_id):
        if student_id in self.students:
            return self.students[student_id]
        else:
            print(f"Student with ID {student_id} not found")
            return None
    
    def get_professor(self, professor_id):
        if professor_id in self.professors:
            return self.professors[professor_id]
        else:
            print(f"Professor with ID {professor_id} not found")
            return None
    
    def get_department(self, department_name):
        if department_name in self.departments:
            return self.departments[department_name]
        else:
            print(f"Department {department_name} not found")
            return None
        
    def get_all_students(self):
        return list(self.students.values())
    
    def get_all_professors(self):
        return list(self.professors.values())
    
    def to_dict(self):
        return {
            "name": self.name,
            "departments": {name: department.to_dict() for name, department in self.departments.items()},
            "students": {student_id: student.to_dict() for student_id, student in self.students.items()},
            "professors": {professor_id: professor.to_dict() for professor_id, professor in self.professors.items()},
        }
    
    @classmethod
    def from_dict(cls, data):
        college = cls(data["name"])
        return college
