"""
CPU Scheduling Simulation Program
Eulogio Amang Rodriguez Institute of Science and Technology
Activity: CPU Scheduling Algorithms

This is the polished version matching the academic assignment format.
Implements: FCFS, SJF, Priority, Round Robin, Preemptive SJF, Preemptive Priority
"""

import csv
from collections import deque
from typing import List, Tuple


class Process:
    """Represents a process with scheduling information."""
    def __init__(self, pid: int, burst_time: int, arrival_time: int = 0, priority: int = 0):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


class CPUScheduler:
    """CPU Scheduling Simulator with multiple algorithms."""
    
    def __init__(self, processes: List[Process]):
        self.original_processes = processes
        self.processes = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                         for p in processes]
        self.gantt_chart = []
        self.algorithm_name = ""
    
    def reset_processes(self):
        """Reset processes for a new scheduling algorithm."""
        self.processes = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                         for p in self.original_processes]
        self.gantt_chart = []
    
    def fcfs(self) -> Tuple[List, float, float]:
        """First Come First Serve (FCFS) Scheduling."""
        self.reset_processes()
        self.algorithm_name = "FCFS (First Come First Serve)"
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        
        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        return self.gantt_chart, *self._calculate_averages()
    
    def sjf_non_preemptive(self) -> Tuple[List, float, float]:
        """Shortest Job First (Non-preemptive) Scheduling."""
        self.reset_processes()
        self.algorithm_name = "SJF (Shortest Job First) - Non-preemptive"
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        completed = []
        
        while len(completed) < len(self.processes):
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time and p not in completed]
            
            if not available:
                next_arrival = min((p.arrival_time for p in self.processes if p not in completed), 
                                  default=current_time)
                current_time = next_arrival
                continue
            
            process = min(available, key=lambda p: p.burst_time)
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
            completed.append(process)
        
        return self.gantt_chart, *self._calculate_averages()
    
    def priority_non_preemptive(self) -> Tuple[List, float, float]:
        """Priority Scheduling (Non-preemptive, lower number = higher priority)."""
        self.reset_processes()
        self.algorithm_name = "Priority Scheduling - Non-preemptive"
        current_time = 0
        completed = []
        
        while len(completed) < len(self.processes):
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time and p not in completed]
            
            if not available:
                next_arrival = min((p.arrival_time for p in self.processes if p not in completed), 
                                  default=current_time)
                current_time = next_arrival
                continue
            
            process = min(available, key=lambda p: p.priority)
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
            completed.append(process)
        
        return self.gantt_chart, *self._calculate_averages()
    
    def round_robin(self, time_quantum: int = 4) -> Tuple[List, float, float]:
        """Round Robin (RR) Scheduling."""
        self.reset_processes()
        self.algorithm_name = f"Round Robin (Time Quantum = {time_quantum})"
        queue = deque()
        current_time = 0
        processes_by_arrival = sorted(self.processes, key=lambda p: p.arrival_time)
        
        queue.append(processes_by_arrival[0])
        remaining_processes = deque(processes_by_arrival[1:])
        
        while queue:
            process = queue.popleft()
            
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            execution_time = min(time_quantum, process.remaining_time)
            start_time = current_time
            current_time += execution_time
            process.remaining_time -= execution_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
            
            while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                queue.append(remaining_processes.popleft())
            
            if process.remaining_time > 0:
                queue.append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
        
        return self.gantt_chart, *self._calculate_averages()
    
    def preemptive_sjf(self) -> Tuple[List, float, float]:
        """Preemptive Shortest Job First Scheduling."""
        self.reset_processes()
        self.algorithm_name = "Preemptive SJF (Shortest Remaining Time First)"
        current_time = 0
        completed_count = 0
        
        while completed_count < len(self.processes):
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min((p.arrival_time for p in self.processes if p.remaining_time > 0), 
                                  default=current_time)
                current_time = next_arrival
                continue
            
            process = min(available, key=lambda p: p.remaining_time)
            start_time = current_time
            current_time += 1
            process.remaining_time -= 1
            
            if not self.gantt_chart or self.gantt_chart[-1][0] != process.pid:
                self.gantt_chart.append((process.pid, start_time, current_time))
            else:
                pid, start, _ = self.gantt_chart[-1]
                self.gantt_chart[-1] = (pid, start, current_time)
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed_count += 1
        
        return self.gantt_chart, *self._calculate_averages()
    
    def preemptive_priority(self) -> Tuple[List, float, float]:
        """Preemptive Priority Scheduling (lower number = higher priority)."""
        self.reset_processes()
        self.algorithm_name = "Preemptive Priority Scheduling"
        current_time = 0
        completed_count = 0
        
        while completed_count < len(self.processes):
            available = [p for p in self.processes 
                        if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min((p.arrival_time for p in self.processes if p.remaining_time > 0), 
                                  default=current_time)
                current_time = next_arrival
                continue
            
            process = min(available, key=lambda p: p.priority)
            start_time = current_time
            current_time += 1
            process.remaining_time -= 1
            
            if not self.gantt_chart or self.gantt_chart[-1][0] != process.pid:
                self.gantt_chart.append((process.pid, start_time, current_time))
            else:
                pid, start, _ = self.gantt_chart[-1]
                self.gantt_chart[-1] = (pid, start, current_time)
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed_count += 1
        
        return self.gantt_chart, *self._calculate_averages()
    
    def _calculate_averages(self) -> Tuple[float, float]:
        """Calculate average waiting time and turnaround time."""
        total_wt = sum(p.waiting_time for p in self.processes)
        total_tat = sum(p.turnaround_time for p in self.processes)
        avg_wt = total_wt / len(self.processes)
        avg_tat = total_tat / len(self.processes)
        return avg_wt, avg_tat
    
    def display_results(self):
        """Display results in academic format."""
        print(f"\n{self.algorithm_name}")
        print("=" * 90)
        
        print(f"\n{'PROCESS':<10} {'BURST TIME':<15} {'ARRIVAL':<12} {'COMPLETION':<15} "
              f"{'WAITING':<12} {'TURNAROUND':<12}")
        print("-" * 90)
        
        for process in sorted(self.processes, key=lambda p: p.pid):
            print(f"P{process.pid:<9} {process.burst_time:<15} {process.arrival_time:<12} "
                  f"{process.completion_time:<15} {process.waiting_time:<12.1f} "
                  f"{process.turnaround_time:<12.1f}")
        
        avg_wt, avg_tat = self._calculate_averages()
        print("-" * 90)
        print(f"Average Waiting Time: {avg_wt:.2f} units")
        print(f"Average Turnaround Time: {avg_tat:.2f} units")
        
        self._print_gantt_chart()
    
    def _print_gantt_chart(self):
        """Print Gantt Chart visualization."""
        print("\nGANTT CHART:")
        print("|", end="")
        for pid, start, end in self.gantt_chart:
            print(f" P{pid:<2} |", end="")
        print()
        
        print(self.gantt_chart[0][1], end="")
        for pid, start, end in self.gantt_chart:
            padding = len(str(end)) - 1
            print(f"{' ' * (padding)}{end}", end="")
        print("\n")
    
    def export_to_csv(self, filename: str):
        """Export results to CSV file."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Process', 'Burst Time', 'Arrival Time', 'Completion Time', 
                           'Waiting Time', 'Turnaround Time'])
            for process in sorted(self.processes, key=lambda p: p.pid):
                writer.writerow([f'P{process.pid}', process.burst_time, process.arrival_time,
                               process.completion_time, process.waiting_time, 
                               process.turnaround_time])
        print(f"[EXPORT] Results saved to: {filename}")


def print_header():
    """Print assignment header."""
    print("\n" + "=" * 90)
    print("EULOGIO AMANG RODRIGUEZ INSTITUTE OF SCIENCE AND TECHNOLOGY")
    print("Nagtahan, Manila")
    print("\nActivity: CPU Scheduling Algorithms Simulation")
    print("Course Subject: Operating Systems")
    print("=" * 90)


def get_user_input() -> List[Process]:
    """Get process input from user."""
    print("\nEnter number of processes: ", end="")
    n = int(input())
    processes = []
    
    print(f"\nEnter details for {n} processes:")
    print("(Process ID, Burst Time, Arrival Time, Priority)")
    
    for i in range(n):
        print(f"\nProcess {i+1}:")
        pid = int(input("  Process ID: "))
        burst = int(input("  Burst Time: "))
        arrival = int(input("  Arrival Time: "))
        priority = int(input("  Priority (lower = higher): "))
        
        processes.append(Process(pid, burst, arrival, priority))
    
    return processes


def main():
    """Main execution function."""
    print_header()
    
    # Example from activity document
    print("\n[SAMPLE INPUT FROM ACTIVITY]")
    print("\nPROCESS DATA:")
    print("-" * 60)
    print(f"{'Process':<10} {'Burst Time':<15} {'Arrival Time':<15} {'Priority':<15}")
    print("-" * 60)
    
    processes = [
        Process(1, 8, 0, 3),
        Process(2, 4, 1, 1),
        Process(3, 2, 2, 3),
        Process(4, 1, 3, 2),
    ]
    
    for p in processes:
        print(f"P{p.pid:<9} {p.burst_time:<15} {p.arrival_time:<15} {p.priority:<15}")
    
    print("\n" + "=" * 90)
    print("SCHEDULING SIMULATION RESULTS")
    print("=" * 90)
    
    # Run all algorithms
    algorithms = [
        ("FCFS", lambda s: s.fcfs()),
        ("SJF (Non-preemptive)", lambda s: s.sjf_non_preemptive()),
        ("Priority (Non-preemptive)", lambda s: s.priority_non_preemptive()),
        ("Round Robin (TQ=2)", lambda s: s.round_robin(2)),
        ("Preemptive SJF", lambda s: s.preemptive_sjf()),
        ("Preemptive Priority", lambda s: s.preemptive_priority()),
    ]
    
    results_summary = []
    
    for algo_name, algo_func in algorithms:
        scheduler = CPUScheduler(processes)
        gantt, avg_wt, avg_tat = algo_func(scheduler)
        scheduler.display_results()
        
        results_summary.append({
            'algorithm': scheduler.algorithm_name,
            'avg_wt': avg_wt,
            'avg_tat': avg_tat
        })
        
        # Export results
        filename = f"scheduling_{algo_name.replace(' ', '_').replace('(', '').replace(')', '').lower()}.csv"
        scheduler.export_to_csv(filename)
        print()
    
    # Summary comparison
    print("\n" + "=" * 90)
    print("SUMMARY COMPARISON")
    print("=" * 90)
    print(f"\n{'Algorithm':<50} {'Avg WT':<15} {'Avg TAT':<15}")
    print("-" * 90)
    
    for result in results_summary:
        print(f"{result['algorithm']:<50} {result['avg_wt']:<15.2f} {result['avg_tat']:<15.2f}")
    
    print("\n" + "=" * 90 + "\n")


if __name__ == "__main__":
    main()
