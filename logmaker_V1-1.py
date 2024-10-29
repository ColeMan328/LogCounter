import tkinter as tk
from tkinter import ttk
import threading
import time

class LogFileCreator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.running = False
        self.frequency1 = 1.0  # Default frequency for first string
        self.frequency2 = 1.0  # Default frequency for second string
        self.message1 = "Message 1"  # Default content for first log message
        self.message2 = "Message 2"  # Default content for second log message

        self.root = tk.Tk()
        self.root.title("Log File Creator")
        self.root.geometry("300x300")

        self.label1 = ttk.Label(self.root, text="String 1 Frequency (s):")
        self.label1.pack(pady=5)
        self.entry_frequency1 = ttk.Entry(self.root)
        self.entry_frequency1.insert(0, str(self.frequency1))
        self.entry_frequency1.pack(pady=5)

        self.label2 = ttk.Label(self.root, text="String 2 Frequency (s):")
        self.label2.pack(pady=5)
        self.entry_frequency2 = ttk.Entry(self.root)
        self.entry_frequency2.insert(0, str(self.frequency2))
        self.entry_frequency2.pack(pady=5)

        self.label3 = ttk.Label(self.root, text="String 1 Content:")
        self.label3.pack(pady=5)
        self.entry_message1 = ttk.Entry(self.root)
        self.entry_message1.insert(0, self.message1)
        self.entry_message1.pack(pady=5)

        self.label4 = ttk.Label(self.root, text="String 2 Content:")
        self.label4.pack(pady=5)
        self.entry_message2 = ttk.Entry(self.root)
        self.entry_message2.insert(0, self.message2)
        self.entry_message2.pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_logging)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_logging)
        self.stop_button.pack(pady=10)

    def write_log(self, message, frequency):
        while self.running:
            with open(self.file_path, 'a') as file:
                file.write(f"{message}\n")
            time.sleep(frequency)

    def start_logging(self):
        try:
            self.frequency1 = float(self.entry_frequency1.get())
            self.frequency2 = float(self.entry_frequency2.get())
        except ValueError:
            print("Please enter valid numbers for frequencies.")
            return

        self.message1 = self.entry_message1.get()
        self.message2 = self.entry_message2.get()

        if not self.running:
            self.running = True
            threading.Thread(target=self.write_log, args=(self.message1, self.frequency1), daemon=True).start()
            threading.Thread(target=self.write_log, args=(self.message2, self.frequency2), daemon=True).start()

    def stop_logging(self):
        self.running = False

    def run(self):
        self.root.mainloop()

# Usage
log_file_path = 'activity.log'  # Path to the file where logs will be written

log_creator = LogFileCreator(log_file_path)
log_creator.run()