import java.io.*;
import java.time.*;
import java.util.*;

public class AttendanceSystem {
    private static final String EMP_FILE = "employees.dat";
    private static final String ATT_FILE = "attendance.dat";
    private Set<String> employees = new HashSet<>();
    private Map<LocalDate, Map<String, String>> records = new HashMap<>();

    public AttendanceSystem() {
        loadData();
    }

    private void loadData() {
        try {
            ObjectInputStream ois = new ObjectInputStream(new FileInputStream(EMP_FILE));
            employees = (Set<String>) ois.readObject();
            ois = new ObjectInputStream(new FileInputStream(ATT_FILE));
            records = (Map<LocalDate, Map<String, String>>) ois.readObject();
        } catch (Exception e) {
            System.out.println("No existing data found or error loading: " + e.getMessage());
        }
    }

    private void saveData() {
        try {
            ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(EMP_FILE));
            oos.writeObject(employees);
            oos = new ObjectOutputStream(new FileOutputStream(ATT_FILE));
            oos.writeObject(records);
        } catch (IOException e) {
            System.err.println("Error saving data: " + e.getMessage());
        }
    }

    public void addEmployee(String name) {
        if (employees.add(name)) {
            saveData();
            System.out.println(name + " added.");
        } else System.out.println(name + " exists.");
    }

    public void markAttendance(LocalDate date) {
        date = date != null ? date : LocalDate.now();
        records.putIfAbsent(date, new HashMap<>());
        
        if (date.getDayOfWeek() == DayOfWeek.SUNDAY) {
            employees.forEach(e -> records.get(date).put(e, "Sunday"));
            saveData();
            System.out.println("Sunday - all marked.");
            return;
        }

        Scanner sc = new Scanner(System.in);
        employees.forEach(emp -> {
            if (!records.get(date).containsKey(emp)) {
                System.out.printf("%s on %s:\n1.Present 2.Absent 3.Leave 4.Holiday: ", emp, date);
                String status = switch(sc.nextLine()) {
                    case "1" -> "Present";
                    case "3" -> "Leave";
                    case "4" -> "Holiday";
                    default -> "Absent";
                };
                records.get(date).put(emp, status);
                System.out.println(emp + ": " + status);
            } else System.out.println(emp + " already marked.");
        });
        saveData();
    }

    public void viewData(YearMonth month, String emp) {
        System.out.println("\nATTENDANCE RECORDS");
        records.entrySet().stream()
            .filter(e -> month == null || YearMonth.from(e.getKey()).equals(month))
            .sorted(Map.Entry.comparingByKey())
            .forEach(e -> {
                System.out.printf("\n%s (%s):\n", e.getKey(), e.getKey().getDayOfWeek());
                e.getValue().entrySet().stream()
                    .filter(v -> emp == null || v.getKey().equals(emp))
                    .forEach(v -> System.out.println("  " + v.getKey() + ": " + v.getValue()));
            });
    }

    public void generateReport(YearMonth month) {
        System.out.println("\nREPORT" + (month != null ? " FOR " + month : ""));
        employees.forEach(emp -> {
            System.out.println("\n" + emp + ":");
            records.entrySet().stream()
                .filter(e -> month == null || YearMonth.from(e.getKey()).equals(month))
                .flatMap(e -> e.getValue().entrySet().stream())
                .filter(e -> e.getKey().equals(emp))
                .collect(Collectors.groupingBy(
                    Map.Entry::getValue, 
                    Collectors.counting()))
                .forEach((status, count) -> System.out.println("  " + status + ": " + count));
        });
    }

    public void deleteAll() {
        employees.clear();
        records.clear();
        new File(EMP_FILE).delete();
        new File(ATT_FILE).delete();
        System.out.println("All data deleted.");
    }

    public static void main(String[] args) {
        AttendanceSystem sys = new AttendanceSystem();
        Scanner sc = new Scanner(System.in);
        
        while (true) {
            System.out.println("\n1.Add 2.Mark 3.View 4.Report 5.Delete 6.Exit");
            switch (sc.nextLine()) {
                case "1" -> {
                    System.out.print("Name: ");
                    sys.addEmployee(sc.nextLine());
                }
                case "2" -> {
                    System.out.print("Date (YYYY-MM-DD) or blank: ");
                    String date = sc.nextLine();
                    sys.markAttendance(date.isEmpty() ? null : LocalDate.parse(date));
                }
                case "3" -> {
                    System.out.print("Filter by (1.Month 2.Employee 3.No filter): ");
                    String choice = sc.nextLine();
                    if (choice.equals("1")) {
                        System.out.print("Month (YYYY-MM): ");
                        sys.viewData(YearMonth.parse(sc.nextLine()), null);
                    } else if (choice.equals("2")) {
                        System.out.print("Employee: ");
                        sys.viewData(null, sc.nextLine());
                    } else sys.viewData(null, null);
                }
                case "4" -> {
                    System.out.print("Month (YYYY-MM) or blank: ");
                    String month = sc.nextLine();
                    sys.generateReport(month.isEmpty() ? null : YearMonth.parse(month));
                }
                case "5" -> {
                    System.out.print("Confirm delete ALL? (yes): ");
                    if (sc.nextLine().equalsIgnoreCase("yes")) sys.deleteAll();
                }
                case "6" -> {
                    System.out.println("Exiting...");
                    sc.close();
                    return;
                }
                default -> System.out.println("Invalid choice!");
            }
        }
    }
}