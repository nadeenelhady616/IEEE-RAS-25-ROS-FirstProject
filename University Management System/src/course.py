
class Course:
    def __init__(self, course_code, course_name, credits, level):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.level = level
        self.enrolled_students = {}
        self.professor = None

    
    def assign_professor(self, professor_id):
        self.professor = professor_id
        print(f"Professor {professor_id} assigned to course {self.course_code}")
        return True
    
    def no_enrolled(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.max_students
   
    def to_dict(self):
        return {
            "course_code": self.course_code,
            "course_name": self.course_name,
            "credits": self.credits,
            "level": self.level,
            "enrolled_students": self.enrolled_students,
            "professor": self.professor
        }
    def from_dict(data):
        return Course(
            course_code=data["course_code"],
            course_name=data["course_name"],
            credits=data["credits"],
            level=data["level"]
        )