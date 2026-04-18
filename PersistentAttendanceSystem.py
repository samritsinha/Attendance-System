import datetime
import csv
import os

class AttendanceSystem:
    def __init__(self):
        self.employees = []
        self.attendance_records = {}
        self.load_employees()
        self.load_attendance()

    def load_employees(self):
        """Load employees from a CSV file if it exists"""
        if os.path.exists('employees.csv'):
            with open('employees.csv', 'r') as file:
                reader = csv.reader(file)
                self.employees = [row[0] for row in reader]

    def save_employees(self):
        """Save employees to a CSV file"""
        with open('employees.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for employee in self.employees:
                writer.writerow([employee])

    def load_attendance(self):
        """Load attendance records from a CSV file if it exists"""
        if os.path.exists('attendance.csv'):
            with open('attendance.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = row['Date']
                    if date not in self.attendance_records:
                        self.attendance_records[date] = {}
                    self.attendance_records[date][row['Employee']] = row['Status']

    def save_attendance(self):
        """Save attendance records to a CSV file"""
        with open('attendance.csv', 'w', newline='') as file:
            fieldnames = ['Date', 'Employee', 'Status', 'Day', 'Month', 'Year']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for date in self.attendance_records:
                for employee in self.attendance_records[date]:
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                    writer.writerow({
                        'Date': date,
                        'Employee': employee,
                        'Status': self.attendance_records[date][employee],
                        'Day': date_obj.day,
                        'Month': date_obj.month,
                        'Year': date_obj.year
                    })

    def add_employee(self, name):
        """Add a new employee to the system"""
        if name not in self.employees:
            self.employees.append(name)
            self.save_employees()
            print(f"Employee {name} added successfully.")
        else:
            print(f"Employee {name} already exists.")

    def mark_attendance(self, date=None):
        """Mark attendance for all employees on a specific date"""
        if date is None:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        
        date_str = date.strftime('%Y-%m-%d')
        weekday = date.strftime('%A')
        
        if date_str not in self.attendance_records:
            self.attendance_records[date_str] = {}
        
        print(f"\nMarking attendance for {date_str} ({weekday})")
        
        for employee in self.employees:
            if employee in self.attendance_records[date_str]:
                print(f"{employee}: Already marked as {self.attendance_records[date_str][employee]}")
                continue
            
            if weekday == 'Sunday':
                status = 'Sunday'
            else:
                print(f"\nEmployee: {employee}")
                print("1. Present")
                print("2. Absent")
                print("3. Leave")
                print("4. Holiday")
                choice = input("Enter status (1-4): ")
                
                if choice == '1':
                    status = 'Present'
                elif choice == '2':
                    status = 'Absent'
                elif choice == '3':
                    status = 'Leave'
                elif choice == '4':
                    status = 'Holiday'
                else:
                    print("Invalid choice. Defaulting to Absent.")
                    status = 'Absent'
            
            self.attendance_records[date_str][employee] = status
            print(f"{employee} marked as {status}")
        
        self.save_attendance()

    def view_attendance(self, month=None, year=None, employee=None):
        """View attendance records with filters"""
        print("\nAttendance Records")
        print("-----------------")
        
        for date in sorted(self.attendance_records.keys()):
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            
            # Apply filters
            if month and date_obj.month != month:
                continue
            if year and date_obj.year != year:
                continue
                
            weekday = date_obj.strftime('%A')
            print(f"\nDate: {date} ({weekday})")
            
            for emp, status in self.attendance_records[date].items():
                if employee and emp != employee:
                    continue
                print(f"{emp}: {status}")

    def generate_report(self, month=None, year=None):
        """Generate a monthly or yearly attendance report"""
        print("\nAttendance Report")
        print("---------------")
        
        if month and year:
            print(f"For Month: {month}, Year: {year}")
        elif year:
            print(f"For Year: {year}")
        
        employee_stats = {emp: {'Present': 0, 'Absent': 0, 'Leave': 0, 'Holiday': 0, 'Sunday': 0} 
                         for emp in self.employees}
        
        for date in self.attendance_records:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            
            if month and date_obj.month != month:
                continue
            if year and date_obj.year != year:
                continue
                
            for emp, status in self.attendance_records[date].items():
                if status in employee_stats[emp]:
                    employee_stats[emp][status] += 1
        
        for emp in self.employees:
            print(f"\nEmployee: {emp}")
            for status, count in employee_stats[emp].items():
                print(f"{status}: {count}")

def main():
    system = AttendanceSystem()
    
    while True:
        print("\nEmployee Attendance System")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. View Attendance")
        print("4. Generate Report")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter employee name: ")
            system.add_employee(name)
        
        elif choice == '2':
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if date_input:
                system.mark_attendance(date_input)
            else:
                system.mark_attendance()
        
        elif choice == '3':
            print("\nView Attendance Options:")
            print("1. View all records")
            print("2. Filter by month and year")
            print("3. Filter by employee")
            view_choice = input("Enter your choice (1-3): ")
            
            if view_choice == '1':
                system.view_attendance()
            elif view_choice == '2':
                year = int(input("Enter year (e.g., 2023): "))
                month = int(input("Enter month (1-12): "))
                system.view_attendance(month=month, year=year)
            elif view_choice == '3':
                employee = input("Enter employee name: ")
                system.view_attendance(employee=employee)
        
        elif choice == '4':
            print("\nGenerate Report Options:")
            print("1. Monthly report")
            print("2. Yearly report")
            report_choice = input("Enter your choice (1-2): ")
            
            if report_choice == '1':
                year = int(input("Enter year (e.g., 2023): "))
                month = int(input("Enter month (1-12): "))
                system.generate_report(month=month, year=year)
            elif report_choice == '2':
                year = int(input("Enter year (e.g., 2023): "))
                system.generate_report(year=year)
        
        elif choice == '5':
            print("Exiting system...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()