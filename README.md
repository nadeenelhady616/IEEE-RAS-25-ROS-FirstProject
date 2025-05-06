# College Management System (Python Project)

A simple Python-based project that simulates a basic college management system. It includes modules for students, professors, courses, registration, attendance, and grading.

# Project Structure

- `student.py`: Handles student data (course registration, grades, attendance, save/load from file).
- `professor.py`: Manages professor-related actions (assign courses, enter grades, track attendance).
- `course.py`: Represents course information.
- `college.py`: Central hub managing students, professors, and courses.
- `registration.py`: Handles student course registration.
- `attendance.py`: Records attendance.
- `grading.py`: Manages student grading.
- `config.py`: Stores configuration like maximum allowed courses.
- `data.json`: Stores persistent student data.
- `main.py`: Main entry point to run and test the system.

# Requirements

- Python 3.10 or higher
- All files must be in the same folder/directory.

# How to Run the Project

1. Open the project folder in **Visual Studio Code** or any code editor.
2. Make sure Python is installed and configured.
3. Run the `main.py` file:
   - Right-click the file > **Run Python File in Terminal**
   - Or use the terminal:  
     ```bash
     python main.py
     ```

4. You should see output indicating the modules have loaded successfully.

#  Notes

- All data (students, grades, attendance) is stored in `data.json` file.
- You can change settings like the maximum allowed courses inside `config.py`.

# Project Purpose

This project is built for educational purposes to practice:
- Object-Oriented Programming (OOP) in Python
- Working with JSON files for simple data storage
- Organizing code using modular programming

---

