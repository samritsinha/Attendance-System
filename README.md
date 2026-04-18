# 📊 Attendance Management System (Java - CSV Based)

## 📌 Project Overview

The **Attendance Management System** is a console-based Java application designed to manage employee attendance efficiently. It allows users to add employees, mark daily attendance, view records, and generate reports.

The system uses **CSV files** for data storage, making it simple, portable, and easy to view in tools like Microsoft Excel.

---

## 🚀 Features

* ✅ Add new employees
* ✅ Mark daily attendance (Present / Absent / Leave / Holiday)
* ✅ Automatic Sunday marking
* ✅ View attendance records
* ✅ Generate summary reports
* ✅ Persistent data storage using CSV files

---

## 🗂️ Project Structure

```
Attendance System/
│── AttendanceSystem.java   # Main Java program
│── employees.csv           # Stores employee names
│── attendance.csv          # Stores attendance records
│── PersistentAttendanceSystem.py (optional)
```

---

## 💾 Data Storage Format

### employees.csv

```
Samrit
Rahul
Amit
```

### attendance.csv

```
Date,Employee,Status
2026-04-18,Samrit,Present
2026-04-18,Rahul,Absent
```

---

## ⚙️ Technologies Used

* Java (Core Java)
* File Handling (BufferedReader, BufferedWriter)
* Java Time API (LocalDate, YearMonth)
* Collections Framework (HashMap, HashSet)

---

## ▶️ How to Run

1. Open terminal in project folder
2. Compile the program:

   ```
   javac AttendanceSystem.java
   ```
3. Run the program:

   ```
   java AttendanceSystem
   ```

---

## 📋 Menu Options

```
1. Add Employee
2. Mark Attendance
3. View Records
4. Generate Report
5. Exit
```

---

## 📊 Example Output

```
Samrit: Present
Rahul: Absent

REPORT:
Samrit:
  Present: 10
  Absent: 2
```

---

## ⚠️ Notes

* Ensure CSV files are in the same directory as the Java file
* Do not manually edit CSV format incorrectly
* First row of attendance.csv should be:

  ```
  Date,Employee,Status
  ```

---

## 🌟 Future Enhancements

* GUI using Java Swing / JavaFX
* Attendance percentage calculation
* Database integration (MySQL)
* Login authentication system
* Graphical reports and charts

---

## 👨‍💻 Author

**Samrit Sinha**

---

## 📌 Conclusion

This project demonstrates practical implementation of:

* File handling in Java
* Data structures
* Real-world problem solving

It is a simple yet effective system for managing attendance records.

---
