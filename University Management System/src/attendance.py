"""
Attendance module for the University Management System.
Handles attendance tracking for students in courses.
"""

import json
import os
from config import MIN_ATTENDANCE

class Attendance:
    """
    Handles attendance tracking for students in courses.
    """
    
    @staticmethod
    def mark_attendance(course_id, student_id, present, date, filename="data.json"):
        """
        Mark attendance for a student in a course.
        
        Args:
            course_id (str): The ID of the course
            student_id (str): The ID of the student
            present (bool): Whether the student was present
            date (str): The date of the class (YYYY-MM-DD format)
            filename (str): Path to the JSON file
            
        Returns:
            bool: True if attendance marking was successful, False otherwise
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return False
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return False
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return False
            
            student_data = data["students"][student_id]
            
            # Check if student is enrolled in the course
            if course_id not in student_data["courses"]:
                print(f"Student {student_id} is not enrolled in course {course_id}")
                return False
            
            # Initialize attendance record if it doesn't exist
            if "attendance" not in student_data:
                student_data["attendance"] = {}
            
            if course_id not in student_data["attendance"]:
                student_data["attendance"][course_id] = [0, 0]
            
            # Initialize attendance details if it doesn't exist
            if "attendance_details" not in student_data:
                student_data["attendance_details"] = {}
            
            if course_id not in student_data["attendance_details"]:
                student_data["attendance_details"][course_id] = {}
            
            # Mark attendance
            student_data["attendance"][course_id][1] += 1  # Increment total classes
            if present:
                student_data["attendance"][course_id][0] += 1  # Increment attended classes
            
            # Record detailed attendance
            student_data["attendance_details"][course_id][date] = present
            
            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            status = "present" if present else "absent"
            print(f"Marked student {student_id} as {status} for course {course_id} on {date}")
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
    
    @staticmethod
    def get_attendance(student_id, course_id=None, filename="data.json"):
        """
        Get attendance records for a student.
        
        Args:
            student_id (str): The ID of the student
            course_id (str, optional): The ID of the course (if None, get for all courses)
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary with attendance information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if student exists
            if "students" not in data or student_id not in data["students"]:
                print(f"Student {student_id} not found")
                return {}
            
            student_data = data["students"][student_id]
            
            # Check if attendance records exist
            if "attendance" not in student_data:
                print(f"No attendance records for student {student_id}")
                return {}
            
            attendance_data = student_data["attendance"]
            
            if course_id:
                # Get attendance for a specific course
                if course_id not in attendance_data:
                    print(f"No attendance records for student {student_id} in course {course_id}")
                    return {}
                
                attended, total = attendance_data[course_id]
                percentage = (attended / total * 100) if total > 0 else 0
                
                print(f"Attendance for student {student_id} in course {course_id}:")
                print(f"  Attended: {attended}/{total} classes ({percentage:.1f}%)")
                
                # Check if student meets minimum attendance requirement
                if percentage < MIN_ATTENDANCE:
                    print(f"  Warning: Below minimum attendance requirement of {MIN_ATTENDANCE}%")
                
                return {course_id: {"attended": attended, "total": total, "percentage": percentage}}
            else:
                # Get attendance for all courses
                result = {}
                print(f"Attendance for student {student_id} in all courses:")
                
                for c_id, (attended, total) in attendance_data.items():
                    percentage = (attended / total * 100) if total > 0 else 0
                    result[c_id] = {"attended": attended, "total": total, "percentage": percentage}
                    
                    print(f"  Course {c_id}: {attended}/{total} classes ({percentage:.1f}%)")
                    
                    # Check if student meets minimum attendance requirement
                    if percentage < MIN_ATTENDANCE:
                        print(f"    Warning: Below minimum attendance requirement of {MIN_ATTENDANCE}%")
                
                return result
        except Exception as e:
            print(f"Error getting attendance: {e}")
            return {}
    
    @staticmethod
    def get_course_attendance(course_id, filename="data.json"):
        """
        Get attendance records for all students in a course.
        
        Args:
            course_id (str): The ID of the course
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary mapping student IDs to attendance information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # Check if course exists
            if "courses" not in data or course_id not in data["courses"]:
                print(f"Course {course_id} not found")
                return {}
            
            course_data = data["courses"][course_id]
            enrolled_students = course_data["enrolled_students"]
            
            if not enrolled_students:
                print(f"No students enrolled in course {course_id}")
                return {}
            
            result = {}
            print(f"Attendance for all students in course {course_id}:")
            
            for student_id in enrolled_students:
                if student_id in data["students"]:
                    student_data = data["students"][student_id]
                    student_name = student_data["name"]
                    
                    if "attendance" in student_data and course_id in student_data["attendance"]:
                        attended, total = student_data["attendance"][course_id]
                        percentage = (attended / total * 100) if total > 0 else 0
                        
                        result[student_id] = {
                            "name": student_name,
                            "attended": attended,
                            "total": total,
                            "percentage": percentage
                        }
                        
                        print(f"  {student_id} ({student_name}): {attended}/{total} classes ({percentage:.1f}%)")
                        
                        # Check if student meets minimum attendance requirement
                        if percentage < MIN_ATTENDANCE:
                            print(f"    Warning: Below minimum attendance requirement of {MIN_ATTENDANCE}%")
            
            return result
        except Exception as e:
            print(f"Error getting course attendance: {e}")
            return {}
    
    @staticmethod
    def get_attendance_report(filename="data.json"):
        """
        Generate an attendance report for all students in all courses.
        
        Args:
            filename (str): Path to the JSON file
            
        Returns:
            dict: Dictionary with attendance report information
        """
        try:
            # Load data from JSON
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"File {filename} does not exist or is empty")
                return {}
            
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if "students" not in data or "courses" not in data:
                print("No student or course data found")
                return {}
            
            report = {}
            print("Attendance Report:")
            
            for course_id, course_data in data["courses"].items():
                course_name = course_data["course_name"]
                report[course_id] = {"course_name": course_name, "students": {}}
                
                print(f"\nCourse: {course_name} ({course_id})")
                
                for student_id in course_data["enrolled_students"]:
                    if student_id in data["students"]:
                        student_data = data["students"][student_id]
                        student_name = student_data["name"]
                        
                        if "attendance" in student_data and course_id in student_data["attendance"]:
                            attended, total = student_data["attendance"][course_id]
                            percentage = (attended / total * 100) if total > 0 else 0
                            
                            report[course_id]["students"][student_id] = {
                                "name": student_name,
                                "attended": attended,
                                "total": total,
                                "percentage": percentage
                            }
                            
                            print(f"  {student_id} ({student_name}): {attended}/{total} classes ({percentage:.1f}%)")
                            
                            # Check if student meets minimum attendance requirement
                            if percentage < MIN_ATTENDANCE:
                                print(f"    Warning: Below minimum attendance requirement of {MIN_ATTENDANCE}%")
            
            return report
        except Exception as e:
            print(f"Error generating attendance report: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Create a sample data.json file if it doesn't exist
    if not os.path.exists("data.json"):
        sample_data = {
            "students": {
                "S12345": {
                    "name": "John Doe",
                    "student_id": "S12345",
                    "level": "Sophomore",
                    "courses": ["CS101"],
                    "grades": {},
                    "attendance": {}
                }
            },
            "courses": {
                "CS101": {
                    "course_id": "CS101",
                    "course_name": "Introduction to Computer Science",
                    "max_students": 30,
                    "credits": 4,
                    "professor_id": "P54321",
                    "enrolled_students": ["S12345"]
                }
            }
        }
        
        with open("data.json", 'w') as file:
            json.dump(sample_data, file, indent=4)
    
    # Mark attendance for a student
    Attendance.mark_attendance("CS101", "S12345", True, "2023-09-01")
    Attendance.mark_attendance("CS101", "S12345", False, "2023-09-08")
    Attendance.mark_attendance("CS101", "S12345", True, "2023-09-15")
    
    # Get attendance for a student in a course
    Attendance.get_attendance("S12345", "CS101")
    
    # Get attendance for all students in a course
    Attendance.get_course_attendance("CS101")
    
    # Generate attendance report
    Attendance.get_attendance_report()

print("Attendance module loaded successfully")