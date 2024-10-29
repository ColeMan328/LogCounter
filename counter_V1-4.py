import tkinter as tk
from tkinter import ttk
import time
import os
import re
import threading

class LogFileMonitor:
    def __init__(self, file_path, pattern1, pattern2):
        self.file_path = file_path
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.regex1 = re.compile(rf"{self.pattern1}\s+(-?\d+)")
        self.regex2 = re.compile(rf"{self.pattern2}\s+(-?\d+)")
        self.valid_numbers = {"1", "3", "89"}
        self.count1 = 0
        self.count2 = 0
        self.position = 0
        self.running = True
        self.flashing = False

        self.root = tk.Tk()
        self.root.title("Log Monitor")
        self.root.geometry("200x180")
        self.root.attributes('-topmost', True)

        self.label1 = ttk.Label(self.root, text=f"Count1: {self.count1}", font=("Helvetica", 14))
        self.label1.pack(pady=10)

        self.label2 = ttk.Label(self.root, text=f"Count2: {self.count2}", font=("Helvetica", 14))
        self.label2.pack(pady=10)

        self.alert_label = ttk.Label(self.root, text="Alert!", font=("Helvetica", 14), foreground="red")
        self.alert_label.pack(pady=10)
        self.alert_label.pack_forget()

        self.reset_button = ttk.Button(self.root, text="Reset Counts", command=self.reset_counts)
        self.reset_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.stop_running)

    def monitor_log_file(self):
        while self.running:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                file.seek(self.position)
                new_lines = file.readlines()
                self.position = file.tell()

                for line in new_lines:
                    # Match for pattern1 followed by valid numbers
                    match1 = self.regex1.search(line)
                    if match1 and match1.group(1) in self.valid_numbers:
                        self.count1 += 1

                    # Match for pattern2 followed by valid numbers
                    match2 = self.regex2.search(line)
                    if match2 and match2.group(1) in self.valid_numbers:
                        self.count2 += 1

            self.update_ui()
            time.sleep(1)

    def update_ui(self):
        self.label1.config(text=f"Count1: {self.count1}")
        self.label2.config(text=f"Count2: {self.count2}")
        self.check_alert_conditions()
        self.root.update()

    def reset_counts(self):
        self.count1 = 0
        self.count2 = 0
        self.flashing = False
        self.root.config(bg="SystemButtonFace")
        self.alert_label.pack_forget()
        self.update_ui()

    def check_alert_conditions(self):
        if self.count1 >= 10 or self.count2 >= 15 or (self.count1 + self.count2) >= 20:
            if not self.flashing:
                self.start_flashing()
        else:
            self.root.config(bg="SystemButtonFace")
            self.alert_label.pack_forget()
            self.flashing = False

    def start_flashing(self):
        self.flashing = True
        self.flash()

    def flash(self):
        if self.flashing:
            current_color = self.root.cget("bg")
            self.root.config(bg="red" if current_color == "SystemButtonFace" else "SystemButtonFace")
            self.alert_label.pack() if current_color == "SystemButtonFace" else self.alert_label.pack_forget()
            self.root.after(500, self.flash)

    def stop_running(self):
        self.running = False
        self.root.quit()

    def run(self):
        threading.Thread(target=self.monitor_log_file, daemon=True).start()
        self.root.mainloop()

# Example usage
log_file_path = 'example.log'  # Path to your log file
string_to_count1 = 'disp1\\tdiap2\\tdisp3\\tdisp4'  # First string pattern to count
string_to_count2 = 'another pattern\\tother patterns'  # Second string pattern to count

monitor = LogFileMonitor(log_file_path, string_to_count1, string_to_count2)
monitor.run()