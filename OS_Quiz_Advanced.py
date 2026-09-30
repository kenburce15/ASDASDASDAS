"""
Operating Systems Quiz - 50 Questions
Clean, Compact Study Format
Perfect for memorizing and quick review
"""

import os
from datetime import datetime


class OSQuiz:
    """50-Question OS Quiz with Clean Interface"""
    
    QUESTIONS = [
        # MULTIPLE CHOICE (1-30)
        {"num": 1, "type": "MC", "q": "Which OS function manages processes?", 
         "opts": ["A) Memory Management", "B) Process Management", "C) File Management", "D) I/O Management"],
         "ans": "B"},
        
        {"num": 2, "type": "MC", "q": "When does a program become a process?",
         "opts": ["A) When compiled", "B) When loaded into memory and executed", "C) When saved as .exe", "D) When scheduled"],
         "ans": "B"},
        
        {"num": 3, "type": "MC", "q": "Which is NOT a process component?",
         "opts": ["A) Program Code", "B) Heap", "C) Cache Memory", "D) Stack"],
         "ans": "C"},
        
        {"num": 4, "type": "MC", "q": "What state is a process waiting for I/O?",
         "opts": ["A) Ready", "B) Running", "C) Waiting/Blocked", "D) Terminated"],
         "ans": "C"},
        
        {"num": 5, "type": "MC", "q": "Data structure storing process info is called?",
         "opts": ["A) PCB", "B) PID", "C) Stack Frame", "D) Scheduler"],
         "ans": "A"},
        
        {"num": 6, "type": "MC", "q": "Example of parent creating child processes?",
         "opts": ["A) Word opening document", "B) Chrome creating tabs", "C) MATLAB running script", "D) Zoom meeting"],
         "ans": "B"},
        
        {"num": 7, "type": "MC", "q": "Context switching involves?",
         "opts": ["A) Saving/loading process states", "B) Allocating memory", "C) Creating process", "D) Terminating process"],
         "ans": "A"},
        
        {"num": 8, "type": "MC", "q": "Disadvantage of context switching?",
         "opts": ["A) Enables multitasking", "B) CPU overhead", "C) Faster execution", "D) Better responsiveness"],
         "ans": "B"},
        
        {"num": 9, "type": "MC", "q": "A thread is?",
         "opts": ["A) Program on disk", "B) Smallest CPU execution unit", "C) Process waiting for I/O", "D) Scheduling algorithm"],
         "ans": "B"},
        
        {"num": 10, "type": "MC", "q": "Which is FALSE about threads?",
         "opts": ["A) Share process code", "B) Have own stack", "C) Heavier than processes", "D) Managed by scheduler"],
         "ans": "C"},
        
        {"num": 11, "type": "MC", "q": "Windows multithreading model?",
         "opts": ["A) Many-to-One", "B) One-to-One", "C) Many-to-Many", "D) Hybrid"],
         "ans": "B"},
        
        {"num": 12, "type": "MC", "q": "Synchronization using counters?",
         "opts": ["A) Mutex", "B) Semaphore", "C) Monitor", "D) Lock Variable"],
         "ans": "B"},
        
        {"num": 13, "type": "MC", "q": "Binary semaphore values?",
         "opts": ["A) 0 or 1", "B) Any integer", "C) True/False", "D) 0 or more"],
         "ans": "A"},
        
        {"num": 14, "type": "MC", "q": "Java synchronized keyword uses?",
         "opts": ["A) Mutex", "B) Semaphore", "C) Monitor", "D) Critical Section"],
         "ans": "C"},
        
        {"num": 15, "type": "MC", "q": "Critical section requires?",
         "opts": ["A) Mutual Exclusion, Progress, Bounded Waiting", "B) Deadlock, Scheduling", "C) File Sharing, I/O", "D) None"],
         "ans": "A"},
        
        {"num": 16, "type": "MC", "q": "Race condition is?",
         "opts": ["A) Multiple processes modify shared data", "B) Process terminated", "C) Threads blocked", "D) Context switch fails"],
         "ans": "A"},
        
        {"num": 17, "type": "MC", "q": "Producers and consumers sharing buffer?",
         "opts": ["A) Dining Philosophers", "B) Readers-Writers", "C) Producer-Consumer", "D) Banker's"],
         "ans": "C"},
        
        {"num": 18, "type": "MC", "q": "In Readers-Writers, writers need?",
         "opts": ["A) Shared access", "B) Exclusive access", "C) No access", "D) Parallel access"],
         "ans": "B"},
        
        {"num": 19, "type": "MC", "q": "Dining Philosophers problem illustrates?",
         "opts": ["A) Deadlock and starvation", "B) Context switching", "C) Thread creation", "D) File system"],
         "ans": "A"},
        
        {"num": 20, "type": "MC", "q": "Process termination is NOT caused by?",
         "opts": ["A) Task completed", "B) User closed app", "C) Fatal error", "D) Waiting for I/O"],
         "ans": "D"},
        
        {"num": 21, "type": "MC", "q": "Deadlock occurs when?",
         "opts": ["A) Processes wait for held resources", "B) Scheduling fails", "C) Threads terminate", "D) Memory insufficient"],
         "ans": "A"},
        
        {"num": 22, "type": "MC", "q": "FCFS executes in order?",
         "opts": ["A) Round Robin", "B) SJF", "C) Priority", "D) Arrival"],
         "ans": "D"},
        
        {"num": 23, "type": "MC", "q": "Round Robin best for?",
         "opts": ["A) Batch systems", "B) Interactive systems", "C) Real-time", "D) None"],
         "ans": "B"},
        
        {"num": 24, "type": "MC", "q": "SJF may cause starvation of?",
         "opts": ["A) Short jobs", "B) Long jobs", "C) High priority", "D) I/O jobs"],
         "ans": "B"},
        
        {"num": 25, "type": "MC", "q": "Fixed-size memory blocks called?",
         "opts": ["A) Paging", "B) Segmentation", "C) Swapping", "D) Fragmentation"],
         "ans": "A"},
        
        {"num": 26, "type": "MC", "q": "Internal fragmentation in?",
         "opts": ["A) Paging", "B) Segmentation", "C) Swapping", "D) Virtual Memory"],
         "ans": "A"},
        
        {"num": 27, "type": "MC", "q": "External fragmentation in?",
         "opts": ["A) Paging", "B) Segmentation", "C) Swapping", "D) Virtual Memory"],
         "ans": "B"},
        
        {"num": 28, "type": "MC", "q": "File allocation with linked blocks?",
         "opts": ["A) Contiguous", "B) Linked", "C) Indexed", "D) Hash"],
         "ans": "B"},
        
        {"num": 29, "type": "MC", "q": "I/O system responsible for?",
         "opts": ["A) Managing I/O devices", "B) Scheduling CPU", "C) Allocating memory", "D) Preventing deadlock"],
         "ans": "A"},
        
        {"num": 30, "type": "MC", "q": "Real-world synchronization example?",
         "opts": ["A) Two ATMs same account", "B) Process waiting CPU", "C) Thread running JS", "D) File on disk"],
         "ans": "A"},
        
        # IDENTIFICATION (31-50)
        {"num": 31, "type": "ID", "q": "Define a process in one line.",
         "ans": "A program in execution"},
        
        {"num": 32, "type": "ID", "q": "Smallest unit of CPU execution?",
         "ans": "Thread"},
        
        {"num": 33, "type": "ID", "q": "OS structure storing process info?",
         "ans": "Process Control Block (PCB)"},
        
        {"num": 34, "type": "ID", "q": "Process loaded in memory, waiting for CPU?",
         "ans": "Ready state"},
        
        {"num": 35, "type": "ID", "q": "Process executing on CPU?",
         "ans": "Running state"},
        
        {"num": 36, "type": "ID", "q": "Process finished execution?",
         "ans": "Terminated state"},
        
        {"num": 37, "type": "ID", "q": "Process waiting for I/O completion?",
         "ans": "Waiting/Blocked state"},
        
        {"num": 38, "type": "ID", "q": "Process swapped out but ready to run?",
         "ans": "Suspend Ready state"},
        
        {"num": 39, "type": "ID", "q": "Process swapped out and waiting for event?",
         "ans": "Suspend Wait state"},
        
        {"num": 40, "type": "ID", "q": "Unique identifier for each process?",
         "ans": "Process ID (PID)"},
        
        {"num": 41, "type": "ID", "q": "CPU switching from one process to another?",
         "ans": "Context Switching"},
        
        {"num": 42, "type": "ID", "q": "Prevents multiple processes accessing shared resources?",
         "ans": "Mutual Exclusion"},
        
        {"num": 43, "type": "ID", "q": "Multiple processes modify shared data simultaneously?",
         "ans": "Race Condition"},
        
        {"num": 44, "type": "ID", "q": "Classical problem involving philosophers?",
         "ans": "Dining Philosophers Problem"},
        
        {"num": 45, "type": "ID", "q": "Classical problem with readers and writers?",
         "ans": "Readers-Writers Problem"},
        
        {"num": 46, "type": "ID", "q": "Classical problem with producers/consumers?",
         "ans": "Producer-Consumer Problem"},
        
        {"num": 47, "type": "ID", "q": "Locking mechanism allowing one thread?",
         "ans": "Mutex"},
        
        {"num": 48, "type": "ID", "q": "Synchronization using counters?",
         "ans": "Semaphore"},
        
        {"num": 49, "type": "ID", "q": "Combines shared data with procedures?",
         "ans": "Monitor"},
        
        {"num": 50, "type": "ID", "q": "Processes wait indefinitely for held resources?",
         "ans": "Deadlock"},
    ]
    
    def __init__(self):
        self.score = 0
        self.answers = []
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Print quiz header"""
        print("\n" + "="*70)
        print(" "*15 + "OPERATING SYSTEMS QUIZ")
        print(" "*20 + "50 Questions - Study Mode")
        print("="*70 + "\n")
    
    def print_question(self, q):
        """Print a single question in compact format"""
        print(f"\n┌─ Q{q['num']:2d} [{q['type']}] {'─'*55}")
        print(f"│ {q['q']}")
        
        if q['type'] == 'MC':
            print(f"│")
            for opt in q['opts']:
                print(f"│  {opt}")
        
        print(f"└{'─'*66}\n")
    
    def display_answer(self, q):
        """Display correct answer"""
        if q['type'] == 'MC':
            print(f"   ✓ ANSWER: {q['ans']}\n")
        else:
            print(f"   ✓ ANSWER: {q['ans']}\n")
    
    def run_interactive_mode(self):
        """Interactive quiz mode"""
        self.clear_screen()
        self.print_header()
        
        print("MODE: Interactive Review")
        print("View each question and answer\n")
        input("Press Enter to start...\n")
        
        for i, q in enumerate(self.QUESTIONS, 1):
            self.clear_screen()
            self.print_header()
            print(f"Progress: {i}/{len(self.QUESTIONS)}\n")
            self.print_question(q)
            
            if q['type'] == 'MC':
                user_ans = input("Your answer (A/B/C/D): ").strip().upper()
                if user_ans in ['A', 'B', 'C', 'D']:
                    self.answers.append(user_ans)
                    if user_ans == q['ans'].split(')')[0]:
                        self.score += 1
                        print("✓ CORRECT!")
                    else:
                        print("✗ INCORRECT!")
            else:
                user_ans = input("Your answer: ").strip()
                self.answers.append(user_ans)
                print("(Check against answer key)\n")
            
            self.display_answer(q)
            
            if i < len(self.QUESTIONS):
                input("Press Enter for next question...")
        
        self.show_results()
    
    def run_study_mode(self):
        """Study mode - view all questions with answers"""
        self.clear_screen()
        self.print_header()
        
        print("MODE: Study Review - All Questions with Answers\n")
        input("Press Enter to view all questions and answers...\n")
        
        for q in self.QUESTIONS:
            self.print_question(q)
            self.display_answer(q)
            input("Press Enter to continue...")
            self.clear_screen()
            self.print_header()
        
        self.show_study_summary()
    
    def run_quick_review(self):
        """Quick review - compact view"""
        self.clear_screen()
        print("\n" + "="*70)
        print(" "*15 + "QUICK REFERENCE GUIDE")
        print("="*70 + "\n")
        
        print("MULTIPLE CHOICE ANSWERS (1-30):\n")
        for i in range(1, 31):
            q = self.QUESTIONS[i-1]
            ans_letter = q['ans'].split(')')[0]
            print(f"Q{i:2d}: {ans_letter}  ", end="")
            if i % 5 == 0:
                print()
        
        print("\n\nIDENTIFICATION ANSWERS (31-50):\n")
        for i in range(31, 51):
            q = self.QUESTIONS[i-1]
            print(f"Q{i}: {q['ans']}")
        
        print("\n" + "="*70 + "\n")
    
    def show_results(self):
        """Show quiz results"""
        self.clear_screen()
        percentage = (self.score / 30) * 100  # Only MC counted
        
        print("\n" + "="*70)
        print(" "*25 + "QUIZ RESULTS")
        print("="*70)
        print(f"\n  Score: {self.score}/30 Multiple Choice Questions")
        print(f"  Percentage: {percentage:.1f}%\n")
        
        if percentage >= 90:
            print("  Rating: ★★★★★ EXCELLENT!")
        elif percentage >= 80:
            print("  Rating: ★★★★☆ VERY GOOD!")
        elif percentage >= 70:
            print("  Rating: ★★★☆☆ GOOD")
        elif percentage >= 60:
            print("  Rating: ★★☆☆☆ SATISFACTORY")
        else:
            print("  Rating: ★☆☆☆☆ NEEDS IMPROVEMENT")
        
        print("\n" + "="*70 + "\n")
    
    def show_study_summary(self):
        """Show study mode summary"""
        print("\n" + "="*70)
        print(" "*20 + "STUDY SESSION COMPLETE")
        print("="*70)
        print("\nYou have reviewed all 50 questions.")
        print("Memorize the answers and come back to test yourself!\n")
        print("="*70 + "\n")
    
    def export_quick_guide(self):
        """Export answer guide to file"""
        filename = f"OS_Quiz_AnswerKey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("="*70 + "\n")
            f.write("OPERATING SYSTEMS QUIZ - 50 QUESTIONS\n")
            f.write("Answer Key & Study Guide\n")
            f.write("="*70 + "\n\n")
            
            f.write("MULTIPLE CHOICE (1-30):\n")
            f.write("-"*70 + "\n")
            for i in range(1, 31):
                q = self.QUESTIONS[i-1]
                ans_letter = q['ans'].split(')')[0]
                f.write(f"Q{i:2d}: {ans_letter}  {q['q']}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("IDENTIFICATION (31-50):\n")
            f.write("-"*70 + "\n")
            for i in range(31, 51):
                q = self.QUESTIONS[i-1]
                f.write(f"Q{i}: {q['q']}\n")
                f.write(f"    Answer: {q['ans']}\n\n")
            
            f.write("="*70 + "\n")
        
        print(f"\n✓ Answer key exported to: {filename}\n")
    
    def main_menu(self):
        """Main menu"""
        while True:
            self.clear_screen()
            self.print_header()
            
            print("SELECT MODE:\n")
            print("  1) Interactive Mode - Test yourself")
            print("  2) Study Mode - View all questions")
            print("  3) Quick Reference - Answer key only")
            print("  4) Export Answer Key to File")
            print("  5) Exit\n")
            
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == '1':
                self.run_interactive_mode()
                input("\nPress Enter to return to menu...")
            elif choice == '2':
                self.run_study_mode()
                input("\nPress Enter to return to menu...")
            elif choice == '3':
                self.run_quick_review()
                input("Press Enter to return to menu...")
            elif choice == '4':
                self.export_quick_guide()
                input("Press Enter to return to menu...")
            elif choice == '5':
                print("\nThank you for using OS Quiz. Good luck!\n")
                break
            else:
                print("\n✗ Invalid choice. Try again.")
                input("Press Enter...")


def main():
    """Run quiz"""
    quiz = OSQuiz()
    quiz.main_menu()


if __name__ == "__main__":
    main()
