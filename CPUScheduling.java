import java.util.*;
import java.io.*;

/**
 * CPU Scheduling Simulation Program
 * Eulogio Amang Rodriguez Institute of Science and Technology
 * Activity: CPU Scheduling Algorithms
 * 
 * Implements: FCFS, SJF, Priority, Round Robin, Preemptive SJF, Preemptive Priority
 */

public class CPUScheduling {
    
    static class Process implements Comparable<Process> {
        int pid;
        int burstTime;
        int remainingTime;
        int arrivalTime;
        int priority;
        int completionTime;
        double waitingTime;
        double turnaroundTime;
        
        Process(int pid, int burst, int arrival, int priority) {
            this.pid = pid;
            this.burstTime = burst;
            this.remainingTime = burst;
            this.arrivalTime = arrival;
            this.priority = priority;
            this.completionTime = 0;
            this.waitingTime = 0;
            this.turnaroundTime = 0;
        }
        
        @Override
        public int compareTo(Process other) {
            return Integer.compare(this.pid, other.pid);
        }
    }
    
    static class GanttEntry {
        int pid;
        int start;
        int end;
        
        GanttEntry(int pid, int start, int end) {
            this.pid = pid;
            this.start = start;
            this.end = end;
        }
    }
    
    static class CPUScheduler {
        List<Process> originalProcesses;
        List<Process> processes;
        List<GanttEntry> ganttChart;
        String algorithmName;
        
        CPUScheduler(List<Process> processes) {
            this.originalProcesses = new ArrayList<>();
            for (Process p : processes) {
                this.originalProcesses.add(new Process(p.pid, p.burstTime, p.arrivalTime, p.priority));
            }
            resetProcesses();
        }
        
        void resetProcesses() {
            this.processes = new ArrayList<>();
            for (Process p : originalProcesses) {
                this.processes.add(new Process(p.pid, p.burstTime, p.arrivalTime, p.priority));
            }
            this.ganttChart = new ArrayList<>();
        }
        
        void fcfs() {
            resetProcesses();
            algorithmName = "FCFS (First Come First Serve)";
            processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
            int currentTime = 0;
            
            for (Process process : processes) {
                if (currentTime < process.arrivalTime) {
                    currentTime = process.arrivalTime;
                }
                
                int startTime = currentTime;
                currentTime += process.burstTime;
                process.completionTime = currentTime;
                process.turnaroundTime = process.completionTime - process.arrivalTime;
                process.waitingTime = process.turnaroundTime - process.burstTime;
                
                ganttChart.add(new GanttEntry(process.pid, startTime, currentTime));
            }
        }
        
        void sjfNonPreemptive() {
            resetProcesses();
            algorithmName = "SJF (Shortest Job First) - Non-preemptive";
            processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
            int currentTime = 0;
            int completed = 0;
            
            while (completed < processes.size()) {
                Process selected = null;
                
                for (Process p : processes) {
                    if (p.arrivalTime <= currentTime && p.burstTime != -1) {
                        if (selected == null || p.burstTime < selected.burstTime) {
                            selected = p;
                        }
                    }
                }
                
                if (selected == null) {
                    int minArrival = Integer.MAX_VALUE;
                    for (Process p : processes) {
                        if (p.burstTime != -1 && p.arrivalTime < minArrival) {
                            minArrival = p.arrivalTime;
                        }
                    }
                    currentTime = minArrival;
                    continue;
                }
                
                int startTime = currentTime;
                currentTime += selected.burstTime;
                selected.completionTime = currentTime;
                selected.turnaroundTime = selected.completionTime - selected.arrivalTime;
                selected.waitingTime = selected.turnaroundTime - selected.burstTime;
                
                ganttChart.add(new GanttEntry(selected.pid, startTime, currentTime));
                selected.burstTime = -1;
                completed++;
            }
            
            for (Process p : processes) {
                p.burstTime = p.completionTime - p.turnaroundTime + p.waitingTime;
            }
        }
        
        void priorityNonPreemptive() {
            resetProcesses();
            algorithmName = "Priority Scheduling - Non-preemptive";
            processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
            int currentTime = 0;
            int completed = 0;
            
            while (completed < processes.size()) {
                Process selected = null;
                
                for (Process p : processes) {
                    if (p.arrivalTime <= currentTime && p.burstTime != -1) {
                        if (selected == null || p.priority < selected.priority) {
                            selected = p;
                        }
                    }
                }
                
                if (selected == null) {
                    int minArrival = Integer.MAX_VALUE;
                    for (Process p : processes) {
                        if (p.burstTime != -1 && p.arrivalTime < minArrival) {
                            minArrival = p.arrivalTime;
                        }
                    }
                    currentTime = minArrival;
                    continue;
                }
                
                int startTime = currentTime;
                int burst = selected.burstTime;
                currentTime += burst;
                selected.completionTime = currentTime;
                selected.turnaroundTime = selected.completionTime - selected.arrivalTime;
                selected.waitingTime = selected.turnaroundTime - burst;
                
                ganttChart.add(new GanttEntry(selected.pid, startTime, currentTime));
                selected.burstTime = -1;
                completed++;
            }
            
            for (Process p : processes) {
                if (p.burstTime == -1) {
                    p.burstTime = (int)(p.turnaroundTime - p.waitingTime);
                }
            }
        }
        
        void roundRobin(int timeQuantum) {
            resetProcesses();
            algorithmName = "Round Robin (Time Quantum = " + timeQuantum + ")";
            processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
            
            Queue<Process> queue = new LinkedList<>();
            int currentTime = 0;
            queue.add(processes.get(0));
            
            int idx = 1;
            while (!queue.isEmpty()) {
                Process process = queue.poll();
                
                if (currentTime < process.arrivalTime) {
                    currentTime = process.arrivalTime;
                }
                
                int executionTime = Math.min(timeQuantum, process.remainingTime);
                int startTime = currentTime;
                currentTime += executionTime;
                process.remainingTime -= executionTime;
                
                ganttChart.add(new GanttEntry(process.pid, startTime, currentTime));
                
                while (idx < processes.size() && processes.get(idx).arrivalTime <= currentTime) {
                    queue.add(processes.get(idx));
                    idx++;
                }
                
                if (process.remainingTime > 0) {
                    queue.add(process);
                } else {
                    process.completionTime = currentTime;
                    process.turnaroundTime = process.completionTime - process.arrivalTime;
                    process.waitingTime = process.turnaroundTime - process.burstTime;
                }
            }
        }
        
        void preemptiveSJF() {
            resetProcesses();
            algorithmName = "Preemptive SJF (Shortest Remaining Time First)";
            int currentTime = 0;
            int completed = 0;
            
            while (completed < processes.size()) {
                Process selected = null;
                
                for (Process p : processes) {
                    if (p.arrivalTime <= currentTime && p.remainingTime > 0) {
                        if (selected == null || p.remainingTime < selected.remainingTime) {
                            selected = p;
                        }
                    }
                }
                
                if (selected == null) {
                    int minArrival = Integer.MAX_VALUE;
                    for (Process p : processes) {
                        if (p.remainingTime > 0 && p.arrivalTime < minArrival) {
                            minArrival = p.arrivalTime;
                        }
                    }
                    currentTime = minArrival;
                    continue;
                }
                
                int startTime = currentTime;
                currentTime++;
                selected.remainingTime--;
                
                if (ganttChart.isEmpty() || ganttChart.get(ganttChart.size() - 1).pid != selected.pid) {
                    ganttChart.add(new GanttEntry(selected.pid, startTime, currentTime));
                } else {
                    ganttChart.get(ganttChart.size() - 1).end = currentTime;
                }
                
                if (selected.remainingTime == 0) {
                    selected.completionTime = currentTime;
                    selected.turnaroundTime = selected.completionTime - selected.arrivalTime;
                    selected.waitingTime = selected.turnaroundTime - selected.burstTime;
                    completed++;
                }
            }
        }
        
        void preemptivePriority() {
            resetProcesses();
            algorithmName = "Preemptive Priority Scheduling";
            int currentTime = 0;
            int completed = 0;
            
            while (completed < processes.size()) {
                Process selected = null;
                
                for (Process p : processes) {
                    if (p.arrivalTime <= currentTime && p.remainingTime > 0) {
                        if (selected == null || p.priority < selected.priority) {
                            selected = p;
                        }
                    }
                }
                
                if (selected == null) {
                    int minArrival = Integer.MAX_VALUE;
                    for (Process p : processes) {
                        if (p.remainingTime > 0 && p.arrivalTime < minArrival) {
                            minArrival = p.arrivalTime;
                        }
                    }
                    currentTime = minArrival;
                    continue;
                }
                
                int startTime = currentTime;
                currentTime++;
                selected.remainingTime--;
                
                if (ganttChart.isEmpty() || ganttChart.get(ganttChart.size() - 1).pid != selected.pid) {
                    ganttChart.add(new GanttEntry(selected.pid, startTime, currentTime));
                } else {
                    ganttChart.get(ganttChart.size() - 1).end = currentTime;
                }
                
                if (selected.remainingTime == 0) {
                    selected.completionTime = currentTime;
                    selected.turnaroundTime = selected.completionTime - selected.arrivalTime;
                    selected.waitingTime = selected.turnaroundTime - selected.burstTime;
                    completed++;
                }
            }
        }
        
        void displayResults() {
            System.out.println("\n" + algorithmName);
            System.out.println("=".repeat(100));
            
            System.out.printf("\n%-10s %-15s %-12s %-15s %-12s %-12s\n",
                    "PROCESS", "BURST TIME", "ARRIVAL", "COMPLETION", "WAITING", "TURNAROUND");
            System.out.println("-".repeat(100));
            
            processes.sort(Comparator.comparingInt(p -> p.pid));
            for (Process p : processes) {
                System.out.printf("P%-9d %-15d %-12d %-15d %-12.1f %-12.1f\n",
                        p.pid, p.burstTime, p.arrivalTime, p.completionTime, p.waitingTime, p.turnaroundTime);
            }
            
            double avgWT = processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
            double avgTAT = processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
            
            System.out.println("-".repeat(100));
            System.out.printf("Average Waiting Time: %.2f units\n", avgWT);
            System.out.printf("Average Turnaround Time: %.2f units\n", avgTAT);
            
            printGanttChart();
        }
        
        void printGanttChart() {
            System.out.print("\nGANTT CHART:\n|");
            for (GanttEntry g : ganttChart) {
                System.out.printf(" P%-2d |", g.pid);
            }
            System.out.println();
            
            System.out.print(ganttChart.get(0).start);
            for (GanttEntry g : ganttChart) {
                int padding = String.valueOf(g.end).length() - 1;
                System.out.print(" ".repeat(Math.max(0, padding)) + g.end);
            }
            System.out.println("\n");
        }
        
        void exportToCSV(String filename) throws IOException {
            try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
                writer.println("Process,Burst Time,Arrival Time,Completion Time,Waiting Time,Turnaround Time");
                processes.sort(Comparator.comparingInt(p -> p.pid));
                for (Process p : processes) {
                    writer.printf("P%d,%d,%d,%d,%.1f,%.1f\n",
                            p.pid, p.burstTime, p.arrivalTime, p.completionTime, p.waitingTime, p.turnaroundTime);
                }
            }
            System.out.println("✓ Results exported to: " + filename);
        }
    }
    
    static void printHeader() {
        System.out.println("\n" + "=".repeat(100));
        System.out.println("EULOGIO AMANG RODRIGUEZ INSTITUTE OF SCIENCE AND TECHNOLOGY");
        System.out.println("Nagtahan, Manila");
        System.out.println("\nActivity: CPU Scheduling Algorithms Simulation");
        System.out.println("Course Subject: Operating Systems");
        System.out.println("=".repeat(100));
    }
    
    public static void main(String[] args) throws IOException {
        printHeader();
        
        System.out.println("\n[SAMPLE INPUT FROM ACTIVITY]");
        System.out.println("\nPROCESS DATA:");
        System.out.println("-".repeat(60));
        System.out.printf("%-10s %-15s %-15s %-15s\n", "Process", "Burst Time", "Arrival Time", "Priority");
        System.out.println("-".repeat(60));
        
        List<Process> processes = Arrays.asList(
                new Process(1, 8, 0, 3),
                new Process(2, 4, 1, 1),
                new Process(3, 2, 2, 3),
                new Process(4, 1, 3, 2)
        );
        
        for (Process p : processes) {
            System.out.printf("P%-9d %-15d %-15d %-15d\n", p.pid, p.burstTime, p.arrivalTime, p.priority);
        }
        
        System.out.println("\n" + "=".repeat(100));
        System.out.println("SCHEDULING SIMULATION RESULTS");
        System.out.println("=".repeat(100));
        
        List<String> summaryResults = new ArrayList<>();
        
        // FCFS
        CPUScheduler scheduler = new CPUScheduler(processes);
        scheduler.fcfs();
        scheduler.displayResults();
        double avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        double avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_fcfs.csv");
        
        // SJF Non-preemptive
        scheduler = new CPUScheduler(processes);
        scheduler.sjfNonPreemptive();
        scheduler.displayResults();
        avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_sjf_nonpreemptive.csv");
        
        // Priority Non-preemptive
        scheduler = new CPUScheduler(processes);
        scheduler.priorityNonPreemptive();
        scheduler.displayResults();
        avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_priority_nonpreemptive.csv");
        
        // Round Robin
        scheduler = new CPUScheduler(processes);
        scheduler.roundRobin(2);
        scheduler.displayResults();
        avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_round_robin.csv");
        
        // Preemptive SJF
        scheduler = new CPUScheduler(processes);
        scheduler.preemptiveSJF();
        scheduler.displayResults();
        avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_preemptive_sjf.csv");
        
        // Preemptive Priority
        scheduler = new CPUScheduler(processes);
        scheduler.preemptivePriority();
        scheduler.displayResults();
        avgWT = scheduler.processes.stream().mapToDouble(p -> p.waitingTime).average().orElse(0);
        avgTAT = scheduler.processes.stream().mapToDouble(p -> p.turnaroundTime).average().orElse(0);
        summaryResults.add(String.format("%-50s %-15.2f %-15.2f", scheduler.algorithmName, avgWT, avgTAT));
        scheduler.exportToCSV("scheduling_preemptive_priority.csv");
        
        // Summary
        System.out.println("\n" + "=".repeat(100));
        System.out.println("SUMMARY COMPARISON");
        System.out.println("=".repeat(100));
        System.out.printf("%-50s %-15s %-15s\n", "Algorithm", "Avg WT", "Avg TAT");
        System.out.println("-".repeat(100));
        
        for (String result : summaryResults) {
            System.out.println(result);
        }
        
        System.out.println("\n" + "=".repeat(100));
        System.out.println("REFLECTION:");
        System.out.println("-".repeat(100));
        System.out.println("""
The simulation demonstrates how different CPU scheduling algorithms affect system performance.
FCFS is simple but inefficient, causing high waiting times. SJF minimizes average waiting time
but doesn't account for priority. Priority scheduling ensures important tasks execute first.
Round Robin provides fair distribution but with overhead. Preemptive algorithms respond to
arriving processes dynamically but require more context switching. The choice depends on
system requirements: batch systems prefer SJF, interactive systems prefer Round Robin, and
real-time systems require priority-based scheduling.
        """);
        System.out.println("=".repeat(100) + "\n");
    }
}
