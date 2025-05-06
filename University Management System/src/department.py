class Department:
    def __init__(self, name, courses=None):
        self.name = name
        self.courses = courses if courses is not None else []


    def add_course(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)
        else:
            print(f"Course with code '{course_code}' already exists in '{self.name}'.")
    
    def to_dict(self):
        return {
            "name": self.name,
            "courses": self.courses
        }
    def from_dict(data):
        return Department(
            name=data["name"],
            courses=data["courses"]
        )