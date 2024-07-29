import subprocess
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import csv

class ADBGuiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ADB GUI Tool-SherinJosephRoy")
        self.geometry("800x600")

        self.adb_path = "adb"  # Default to 'adb', change to the full path if necessary

        # Device list frame
        self.device_frame = ctk.CTkFrame(self)
        self.device_frame.pack(pady=10, padx=10, fill="x")

        self.device_label = ctk.CTkLabel(self.device_frame, text="Connected Devices:")
        self.device_label.pack(side="left", padx=10)

        self.update_device_list_button = ctk.CTkButton(self.device_frame, text="Update Device List", command=self.update_device_list)
        self.update_device_list_button.pack(side="right", padx=10)

        self.device_listbox = ctk.CTkTextbox(self, height=100)
        self.device_listbox.pack(pady=10, padx=10, fill="x")

        # Command input frame
        self.command_frame = ctk.CTkFrame(self)
        self.command_frame.pack(pady=10, padx=10, fill="x")

        self.command_input = ctk.CTkEntry(self.command_frame, placeholder_text='Enter ADB Command')
        self.command_input.pack(side="left", fill="x", expand=True, padx=10)

        self.execute_command_button = ctk.CTkButton(self.command_frame, text="Execute Command", command=self.execute_command)
        self.execute_command_button.pack(side="right", padx=10)

        # Dropdown menu for all commands
        self.all_commands = [
            "devices", "logcat -d", "shell getprop", "shell dumpsys battery", "shell pm list packages",
            "shell am start -a android.intent.action.VIEW -d http://www.google.com", "shell input keyevent 26",
            "shell input swipe 300 1000 300 500", "shell screencap -p /sdcard/screenshot.png",
            "shell reboot", "shell settings get system screen_brightness", "shell settings put system screen_brightness 200",
            "shell am startservice", "shell am stopservice", "shell wm size", "shell wm density"
        ]
        self.command_var = ctk.StringVar()
        self.command_dropdown = ctk.CTkComboBox(self.command_frame, variable=self.command_var, values=self.all_commands)
        self.command_dropdown.pack(side="left", padx=10)

        self.execute_dropdown_button = ctk.CTkButton(self.command_frame, text="Execute Selected Command", command=self.execute_selected_command)
        self.execute_dropdown_button.pack(side="left", padx=10)

        # Command output frame
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Command Output:")
        self.output_label.pack(anchor="w", padx=10, pady=5)

        self.output_text = ctk.CTkTextbox(self.output_frame)
        self.output_text.pack(pady=5, padx=10, fill="both", expand=True)

        # Additional features frame
        self.additional_frame = ctk.CTkFrame(self)
        self.additional_frame.pack(pady=10, padx=10, fill="x")

        self.pull_button = ctk.CTkButton(self.additional_frame, text="Pull File", command=self.pull_file)
        self.pull_button.pack(side="left", padx=10)

        self.push_button = ctk.CTkButton(self.additional_frame, text="Push File", command=self.push_file)
        self.push_button.pack(side="left", padx=10)

        self.logcat_button = ctk.CTkButton(self.additional_frame, text="Show Real-time Logcat", command=self.show_realtime_logcat)
        self.logcat_button.pack(side="left", padx=10)

        self.stop_logcat_button = ctk.CTkButton(self.additional_frame, text="Stop Logcat", command=self.stop_realtime_logcat)
        self.stop_logcat_button.pack(side="left", padx=10)

        self.screenshot_button = ctk.CTkButton(self.additional_frame, text="Capture Screenshot", command=self.capture_screenshot)
        self.screenshot_button.pack(side="left", padx=10)

        self.reboot_button = ctk.CTkButton(self.additional_frame, text="Reboot Device", command=self.reboot_device)
        self.reboot_button.pack(side="left", padx=10)

        self.save_log_button = ctk.CTkButton(self.additional_frame, text="Save Logs as CSV", command=self.save_logs_as_csv)
        self.save_log_button.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.stop_logcat = False
        self.logcat_thread = None

    def run_adb_command(self, command):
        try:
            result = subprocess.run([self.adb_path] + command.split(), capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def update_device_list(self):
        self.run_in_thread(self.update_device_list_thread)

    def update_device_list_thread(self):
        output = self.run_adb_command('devices')
        self.device_listbox.delete('1.0', ctk.END)
        self.device_listbox.insert(ctk.END, output)

    def execute_command(self):
        command = self.command_input.get()
        if not command:
            messagebox.showerror("Error", "Please enter a command.")
            return

        self.run_in_thread(self.execute_command_thread, command)

    def execute_command_thread(self, command):
        output = self.run_adb_command(command)
        self.output_text.delete('1.0', ctk.END)
        self.output_text.insert(ctk.END, output)

    def execute_selected_command(self):
        command = self.command_var.get()
        if not command:
            messagebox.showerror("Error", "Please select a command.")
            return

        self.run_in_thread(self.execute_command_thread, command)

    def pull_file(self):
        src_path = ctk.CTkInputDialog(text="Enter source file path on device:", title="Pull File").get_input()
        dest_path = ctk.CTkInputDialog(text="Enter destination path on PC:", title="Pull File").get_input()
        if src_path and dest_path:
            self.run_in_thread(self.pull_file_thread, src_path, dest_path)

    def pull_file_thread(self, src_path, dest_path):
        output = self.run_adb_command(f'pull {src_path} {dest_path}')
        messagebox.showinfo("Pull File", output)

    def push_file(self):
        src_path = ctk.CTkInputDialog(text="Enter source file path on PC:", title="Push File").get_input()
        dest_path = ctk.CTkInputDialog(text="Enter destination path on device:", title="Push File").get_input()
        if src_path and dest_path:
            self.run_in_thread(self.push_file_thread, src_path, dest_path)

    def push_file_thread(self, src_path, dest_path):
        output = self.run_adb_command(f'push {src_path} {dest_path}')
        messagebox.showinfo("Push File", output)

    def show_realtime_logcat(self):
        self.output_text.delete('1.0', ctk.END)
        self.stop_logcat = False
        self.run_in_thread(self.read_logcat)

    def read_logcat(self):
        process = subprocess.Popen([self.adb_path, "logcat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.logcat_process = process
        while not self.stop_logcat:
            line = process.stdout.readline()
            if line:
                self.output_text.insert(ctk.END, line)
                self.output_text.see(ctk.END)
        process.terminate()

    def stop_realtime_logcat(self):
        self.stop_logcat = True
        if self.logcat_thread and self.logcat_thread.is_alive():
            self.logcat_thread.join()

    def capture_screenshot(self):
        self.run_in_thread(self.capture_screenshot_thread)

    def capture_screenshot_thread(self):
        output = self.run_adb_command('shell screencap -p /sdcard/screenshot.png')
        self.output_text.delete('1.0', ctk.END)
        self.output_text.insert(ctk.END, output)
        messagebox.showinfo("Screenshot", "Screenshot captured and saved to /sdcard/screenshot.png")

    def reboot_device(self):
        self.run_in_thread(self.reboot_device_thread)

    def reboot_device_thread(self):
        output = self.run_adb_command('shell reboot')
        self.output_text.delete('1.0', ctk.END)
        self.output_text.insert(ctk.END, output)
        messagebox.showinfo("Reboot", "Device is rebooting...")

    def save_logs_as_csv(self):
        self.run_in_thread(self.save_logs_as_csv_thread)

    def save_logs_as_csv_thread(self):
        logs = self.output_text.get('1.0', ctk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for line in logs.splitlines():
                    writer.writerow([line])
            messagebox.showinfo("Save Logs", f"Logs saved to {file_path}")

    def run_in_thread(self, target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.start()

    def on_closing(self):
        self.stop_logcat = True
        if self.logcat_thread and self.logcat_thread.is_alive():
            self.logcat_thread.join()
        self.destroy()

if __name__ == "__main__":
    app = ADBGuiApp()
    app.mainloop()

