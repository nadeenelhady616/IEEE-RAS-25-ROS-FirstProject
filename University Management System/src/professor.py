class  Professor:
    def __init__(self, name, professor_id, department):
        self.name = name
        self.professor_id = professor_id
        self.department = department
        self.courses = []  # List of course IDs the professor teaches

    def add_course(self, course_id):
        if course_id not in self.courses:
            self.courses.append(course_id)
            print(f"Course {course_id} added to Professor {self.name}'s list.")
        else:
            print(f"Course {course_id} is already in Professor {self.name}'s list.")

    def remove_course(self, course_id):
        if course_id in self.courses:
            self.courses.remove(course_id)
            print(f"Course {course_id} removed from Professor {self.name}'s list.")
        else:
            print(f"Course {course_id} is not in Professor {self.name}'s list.")

    def get_courses(self):
        return self.courses
    
    def to_dict(self):
        return {
            "name": self.name,
            "professor_id": self.professor_id,
            "department": self.department,
            "courses": self.courses
        }
    def from_dict(data):
        return Professor(
            name=data["name"],
            professor_id=data["professor_id"],
            department=data["department"]
        )