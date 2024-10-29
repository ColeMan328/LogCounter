import tkinter as tk
from tkinter import ttk
import time
import os

class LogFileMonitor:
    def __init__(self, file_path, pattern1, pattern2):
        self.file_path = file_path
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.count1 = 0
        self.count2 = 0
        self.position = 0  # Keep track of how far we've read in the file
        self.running = True

        self.root = tk.Tk()
        self.root.title("Log Monitor")
        self.root.geometry("200x150")
        self.root.attributes('-topmost', True)

        self.label1 = ttk.Label(self.root, text=f"Count1: {self.count1}", font=("Helvetica", 14))
        self.label1.pack(pady=10)

        self.label2 = ttk.Label(self.root, text=f"Count2: {self.count2}", font=("Helvetica", 14))
        self.label2.pack(pady=10)

        self.reset_button = ttk.Button(self.root, text="Reset Counts", command=self.reset_counts)
        self.reset_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.stop_running)

    def monitor_log_file(self):
        while self.running:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                # Move the file pointer to the last position we read
                file.seek(self.position)

                # Read new lines
                new_lines = file.readlines()

                # Update file read position
                self.position = file.tell()

                # Count occurrences of the patterns in new lines
                for line in new_lines:
                    if self.pattern1 in line:
                        self.count1 += 1
                    if self.pattern2 in line:
                        self.count2 += 1

            self.update_ui()
            time.sleep(1)  # Check for updates every second

    def update_ui(self):
        self.label1.config(text=f"Count1: {self.count1}")
        self.label2.config(text=f"Count2: {self.count2}")
        self.check_alert_conditions()
        self.root.update()

    def reset_counts(self):
        self.count1 = 0
        self.count2 = 0
        self.update_ui()

    def check_alert_conditions(self):
        if self.count1 >= 10 or self.count2 >= 15 or (self.count1 + self.count2) >= 20:
            self.root.config(bg="red")
        else:
            self.root.config(bg="SystemButtonFace")

    def stop_running(self):
        self.running = False
        self.root.quit()

    def run(self):
        self.root.after(100, self.monitor_log_file)
        self.root.mainloop()

# Example usage
log_file_path = 'activity.log'  # Path to your log file
string_to_count1 = 'disp1\tdiap2\tdisp3\tdisp4'  # First string pattern to count
string_to_count2 = 'some other pattern'  # Second string pattern to count

monitor = LogFileMonitor(log_file_path, string_to_count1, string_to_count2)
monitor.run()