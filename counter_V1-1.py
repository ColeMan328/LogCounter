import tkinter as tk
from tkinter import ttk
import time
import os

class LogFileMonitor:
    def __init__(self, file_path, pattern):
        self.file_path = file_path
        self.pattern = pattern
        self.count = 0
        self.position = 0  # Keep track of how far we've read in the file
        self.running = True

        self.root = tk.Tk()
        self.root.title("Log Monitor")
        self.root.geometry("200x100")
        self.root.attributes('-topmost', True)

        self.label = ttk.Label(self.root, text=f"Count: {self.count}", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.reset_button = ttk.Button(self.root, text="Reset Count", command=self.reset_count)
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

                # Count occurrences of the pattern in new lines
                for line in new_lines:
                    if self.pattern in line:
                        self.count += 1

            self.update_ui()
            time.sleep(1)  # Check for updates every second

    def update_ui(self):
        self.label.config(text=f"Count: {self.count}")
        self.root.update()

    def reset_count(self):
        self.count = 0
        self.update_ui()

    def stop_running(self):
        self.running = False
        self.root.quit()

    def run(self):
        self.root.after(100, self.monitor_log_file)
        self.root.mainloop()

# Example usage
log_file_path = 'activity.log'  # Path to your log file
string_to_count = 'disp1\tdiap2\tdisp3\tdisp4'  # The string pattern to count

monitor = LogFileMonitor(log_file_path, string_to_count)
monitor.run()