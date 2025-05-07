from datetime import datetime
from student_system import Student
from course import Course
import json
class Attendance:

    #mark attendance of a student in a specific course in Professor mode
    def mark_attendance(self, student, course_id, is_present, filename):
        self.attendance_marked = False
        with open(filename, 'r') as file:
            data = json.load(file)
        if student.student_id not in data['students']:
            print(f"Student with ID {student.student_id} not found.")
            return
        if course_id not in student.courses_reg:
            print("Student not enrolled in this course!")
            return
        if course_id not in data['courses']:
            print("Course not found!")
            return

        if 'attendance' not in student.courses_reg[course_id]:
            student.courses[course_id]['attendance'] = []

        date = datetime.now().strftime("%Y-%m-%d")
        student.courses[course_id]['attendance'].append({
            'date': date,
            'present': is_present
        })
        status = "present" if is_present else "absent"
        print(f"Marked {student.name} as {status} on {date}")
        self.attendance_marked = True

    #track attendance of a student in a specific course in student mode
    def track_attendance(self, student, course_id):
        self.attendance_marked = False
        if not student:
            print("Student not found!")
            return None

        if course_id not in student.courses_reg:
            print("Student not enrolled in this course!")
            return None

        attendance = student.courses_reg[course_id].get('attendance', [])
        if not attendance:
            print("No attendance records found")
            return None

        self.attendance_marked = True
        return attendance

  
    