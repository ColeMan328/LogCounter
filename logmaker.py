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
        self.frequency3 = 1.0  # Default frequency for third string
        self.message1 = "Message 1"  # Default content for first log message
        self.message2 = "Message 2"  # Default content for second log message
        self.message3 = "Message 3"  # Default content for third log message

        self.root = tk.Tk()
        self.root.title("Log File Creator")
        self.root.geometry("300x400")

        self.create_ui_element("String 1 Frequency (s):", self.frequency1)
        self.create_ui_element("String 2 Frequency (s):", self.frequency2)
        self.create_ui_element("String 3 Frequency (s):", self.frequency3)
        self.create_ui_element("String 1 Content:", self.message1)
        self.create_ui_element("String 2 Content:", self.message2)
        self.create_ui_element("String 3 Content:", self.message3)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_logging)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_logging)
        self.stop_button.pack(pady=10)

    def create_ui_element(self, label_text, default_value):
        label = ttk.Label(self.root, text=label_text)
        label.pack(pady=5)
        entry = ttk.Entry(self.root)
        entry.insert(0, str(default_value))
        entry.pack(pady=5)
        return entry

    def write_log(self, message, frequency):
        while self.running:
            with open(self.file_path, 'a') as file:
                file.write(f"{message}\n")
            time.sleep(frequency)

    def start_logging(self):
        try:
            self.frequency1 = float(self.entry_frequency1.get())
            self.frequency2 = float(self.entry_frequency2.get())
            self.frequency3 = float(self.entry_frequency3.get())
        except ValueError:
            print("Please enter valid numbers for frequencies.")
            return

        self.message1 = self.entry_message1.get()
        self.message2 = self.entry_message2.get()
        self.message3 = self.entry_message3.get()

        if not self.running:
            self.running = True
            threading.Thread(target=self.write_log, args=(self.message1, self.frequency1), daemon=True).start()
            threading.Thread(target=self.write_log, args=(self.message2, self.frequency2), daemon=True).start()
            threading.Thread(target=self.write_log, args=(self.message3, self.frequency3), daemon=True).start()

    def stop_logging(self):
        self.running = False

    def run(self):
        self.entries = []
        for frequency, message in zip([self.frequency1, self.frequency2, self.frequency3],
                                      [self.message1, self.message2, self.message3]):
            entry = self.create_ui_element("Frequency (s):", frequency)
            self.entries.append(entry)

            entry = self.create_ui_element("Content:", message)
            self.entries.append(entry)

        self.entry_frequency1, self.entry_message1, \
        self.entry_frequency2, self.entry_message2, \
        self.entry_frequency3, self.entry_message3 = self.entries

        self.root.mainloop()

# Usage
log_file_path = 'activity.log'  # Path to the file where logs will be written

log_creator = LogFileCreator(log_file_path)
log_creator.run()