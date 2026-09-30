"""
CPU Scheduling Simulation Program
Eulogio Amang Rodriguez Institute of Science and Technology
Activity: CPU Scheduling Algorithms

This program simulates various CPU scheduling algorithms:
- FCFS (First Come First Serve)
- SJF (Shortest Job First - Non-preemptive)
- Priority Scheduling (Non-preemptive)
- Round Robin
- Preemptive SJF
- Preemptive Priority Scheduling
"""

import csv
from collections import deque
from typing import List, Dict, Tuple
import json


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
    """CPU Scheduling Simulator."""
    
    def __init__(self, processes: List[Process]):
        self.processes = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                         for p in processes]
        self.gantt_chart = []
        self.schedule_results = []
    
    def fcfs(self) -> Tuple[List, float, float]:
        """First Come First Serve Scheduling."""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        self.gantt_chart = []
        
        for process in processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        return self._calculate_averages()
    
    def sjf_non_preemptive(self) -> Tuple[List, float, float]:
        """Shortest Job First (Non-preemptive) Scheduling."""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        completed = []
        self.gantt_chart = []
        
        while processes or completed:
            available = [p for p in processes if p.arrival_time <= current_time]
            
            if not available:
                if processes:
                    current_time = processes[0].arrival_time
                else:
                    break
                continue
            
            # Select process with shortest burst time
            process = min(available, key=lambda p: p.burst_time)
            processes.remove(process)
            
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        return self._calculate_averages()
    
    def priority_non_preemptive(self) -> Tuple[List, float, float]:
        """Priority Scheduling (Non-preemptive, lower number = higher priority)."""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        self.gantt_chart = []
        
        while processes:
            available = [p for p in processes if p.arrival_time <= current_time]
            
            if not available:
                current_time = processes[0].arrival_time
                continue
            
            # Select process with highest priority (lowest priority number)
            process = min(available, key=lambda p: p.priority)
            processes.remove(process)
            
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        return self._calculate_averages()
    
    def round_robin(self, time_quantum: int = 4) -> Tuple[List, float, float]:
        """Round Robin Scheduling."""
        queue = deque()
        current_time = 0
        processes_copy = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                         for p in self.processes]
        self.gantt_chart = []
        
        # Sort by arrival time
        processes_copy.sort(key=lambda p: p.arrival_time)
        
        # Add first arriving process
        if processes_copy:
            queue.append(processes_copy[0])
            processes_copy.pop(0)
        
        while queue:
            process = queue.popleft()
            
            # Handle gap between current time and arrival time
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Execute for time quantum or remaining time
            execution_time = min(time_quantum, process.remaining_time)
            start_time = current_time
            current_time += execution_time
            process.remaining_time -= execution_time
            
            self.gantt_chart.append((process.pid, start_time, current_time))
            
            # Add newly arrived processes to queue
            while processes_copy and processes_copy[0].arrival_time <= current_time:
                queue.append(processes_copy.pop(0))
            
            # If process not finished, add back to queue
            if process.remaining_time > 0:
                queue.append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
        
        return self._calculate_averages()
    
    def preemptive_sjf(self) -> Tuple[List, float, float]:
        """Preemptive Shortest Job First Scheduling."""
        processes = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                    for p in self.processes]
        current_time = 0
        self.gantt_chart = []
        completed_count = 0
        
        while completed_count < len(processes):
            available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min((p.arrival_time for p in processes if p.remaining_time > 0), default=current_time)
                current_time = next_arrival
                continue
            
            # Select process with shortest remaining time
            process = min(available, key=lambda p: p.remaining_time)
            
            start_time = current_time
            current_time += 1  # Execute one unit
            process.remaining_time -= 1
            
            if not self.gantt_chart or self.gantt_chart[-1][0] != process.pid:
                self.gantt_chart.append([process.pid, start_time, current_time])
            else:
                self.gantt_chart[-1][2] = current_time
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed_count += 1
        
        # Convert lists to tuples for consistency
        self.gantt_chart = [tuple(g) for g in self.gantt_chart]
        return self._calculate_averages()
    
    def preemptive_priority(self) -> Tuple[List, float, float]:
        """Preemptive Priority Scheduling (lower number = higher priority)."""
        processes = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) 
                    for p in self.processes]
        current_time = 0
        self.gantt_chart = []
        completed_count = 0
        
        while completed_count < len(processes):
            available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if not available:
                next_arrival = min((p.arrival_time for p in processes if p.remaining_time > 0), default=current_time)
                current_time = next_arrival
                continue
            
            # Select process with highest priority
            process = min(available, key=lambda p: p.priority)
            
            start_time = current_time
            current_time += 1  # Execute one unit
            process.remaining_time -= 1
            
            if not self.gantt_chart or self.gantt_chart[-1][0] != process.pid:
                self.gantt_chart.append([process.pid, start_time, current_time])
            else:
                self.gantt_chart[-1][2] = current_time
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed_count += 1
        
        self.gantt_chart = [tuple(g) for g in self.gantt_chart]
        return self._calculate_averages()
    
    def _calculate_averages(self) -> Tuple[List, float, float]:
        """Calculate average waiting time and turnaround time."""
        total_wt = sum(p.waiting_time for p in self.processes)
        total_tat = sum(p.turnaround_time for p in self.processes)
        avg_wt = total_wt / len(self.processes)
        avg_tat = total_tat / len(self.processes)
        return self.gantt_chart, avg_wt, avg_tat
    
    def print_results(self, algorithm_name: str, time_quantum: int = 0):
        """Print scheduling results in formatted output."""
        print(f"\n{'='*70}")
        print(f"ALGORITHM: {algorithm_name}")
        if time_quantum:
            print(f"Time Quantum: {time_quantum}")
        print(f"{'='*70}")
        
        print(f"\n{'PID':<5} {'Burst':<7} {'Arrival':<8} {'Completion':<12} {'WT':<7} {'TAT':<7}")
        print("-" * 70)
        
        for process in sorted(self.processes, key=lambda p: p.pid):
            print(f"{process.pid:<5} {process.burst_time:<7} {process.arrival_time:<8} "
                  f"{process.completion_time:<12} {process.waiting_time:<7.1f} {process.turnaround_time:<7.1f}")
        
        gantt, avg_wt, avg_tat = self._calculate_averages()
        print("-" * 70)
        print(f"Average Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tat:.2f}")
        
        print(f"\nGantt Chart: {gantt}")
        self._print_gantt_visual()
    
    def _print_gantt_visual(self):
        """Print ASCII representation of Gantt Chart."""
        if not self.gantt_chart:
            return
        
        print("\nGantt Chart Visualization:")
        print("|", end="")
        for pid, start, end in self.gantt_chart:
            print(f" P{pid} |", end="")
        print()
        print(0, end="")
        
        for pid, start, end in self.gantt_chart:
            print(f"{' ' * (len(str(end)) - 1)}{end}", end="")
        print()
    
    def export_to_csv(self, filename: str):
        """Export results to CSV file."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Process ID', 'Burst Time', 'Arrival Time', 'Completion Time', 
                           'Waiting Time', 'Turnaround Time'])
            for process in sorted(self.processes, key=lambda p: p.pid):
                writer.writerow([process.pid, process.burst_time, process.arrival_time,
                               process.completion_time, process.waiting_time, process.turnaround_time])
        print(f"Results exported to {filename}")


def main():
    """Main function to demonstrate CPU scheduling algorithms."""
    
    # Sample input from the activity document
    print("CPU SCHEDULING SIMULATION")
    print("Eulogio Amang Rodriguez Institute of Science and Technology")
    print("="*70)
    
    # Create processes based on sample data from activity
    processes = [
        Process(pid=1, burst_time=8, arrival_time=0, priority=3),
        Process(pid=2, burst_time=4, arrival_time=1, priority=1),
        Process(pid=3, burst_time=2, arrival_time=2, priority=3),
        Process(pid=4, burst_time=1, arrival_time=3, priority=2),
    ]
    
    print("\nInput Processes:")
    print(f"{'PID':<5} {'Burst Time':<12} {'Arrival Time':<14} {'Priority':<10}")
    print("-" * 45)
    for p in processes:
        print(f"{p.pid:<5} {p.burst_time:<12} {p.arrival_time:<14} {p.priority:<10}")
    
    # Run different scheduling algorithms
    
    # FCFS
    scheduler = CPUScheduler(processes)
    scheduler.fcfs()
    scheduler.print_results("First Come First Serve (FCFS)")
    scheduler.export_to_csv("fcfs_results.csv")
    
    # SJF Non-preemptive
    scheduler = CPUScheduler(processes)
    scheduler.sjf_non_preemptive()
    scheduler.print_results("Shortest Job First (SJF) - Non-preemptive")
    scheduler.export_to_csv("sjf_results.csv")
    
    # Priority Non-preemptive
    scheduler = CPUScheduler(processes)
    scheduler.priority_non_preemptive()
    scheduler.print_results("Priority Scheduling - Non-preemptive")
    scheduler.export_to_csv("priority_results.csv")
    
    # Round Robin
    scheduler = CPUScheduler(processes)
    scheduler.round_robin(time_quantum=2)
    scheduler.print_results("Round Robin", time_quantum=2)
    scheduler.export_to_csv("round_robin_results.csv")
    
    # Preemptive SJF
    scheduler = CPUScheduler(processes)
    scheduler.preemptive_sjf()
    scheduler.print_results("Preemptive Shortest Job First (SJF)")
    scheduler.export_to_csv("preemptive_sjf_results.csv")
    
    # Preemptive Priority
    scheduler = CPUScheduler(processes)
    scheduler.preemptive_priority()
    scheduler.print_results("Preemptive Priority Scheduling")
    scheduler.export_to_csv("preemptive_priority_results.csv")


if __name__ == "__main__":
    main()
