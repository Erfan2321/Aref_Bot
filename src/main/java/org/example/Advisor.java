package org.example;

public class Advisor {

    private String name;
    private String status;
    private String workDays;
    private String workHours;

    public Advisor (String name, String status, String workDays, String workHours) {
        this.name = name;
        this.status = status;
        this.workDays = workDays;
        this.workHours = workHours;
    }

    public String getName() { return name; }
    public String getStatus() { return status; }
    public String getWorkDays() { return workDays; }
    public String getWorkHours() { return workHours; }
}
