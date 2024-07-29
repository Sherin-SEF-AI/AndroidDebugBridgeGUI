import subprocess
import customtkinter as ctk
from tkinter import messagebox, filedialog, Toplevel, Label, Button, Scrollbar
import threading
import csv
import pyperclip  # For clipboard operations

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
            ("devices", "List all connected devices"),
            ("logcat -d", "Dump the logcat output"),
            ("shell getprop", "Get system properties"),
            ("shell dumpsys battery", "Get battery status"),
            ("shell pm list packages", "List all installed packages"),
            ("shell am start -a android.intent.action.VIEW -d http://www.google.com", "Open Google in browser"),
            ("shell input keyevent 26", "Toggle screen on/off"),
            ("shell input swipe 300 1000 300 500", "Swipe on screen"),
            ("shell screencap -p /sdcard/screenshot.png", "Take a screenshot"),
            ("shell reboot", "Reboot the device"),
            ("shell settings get system screen_brightness", "Get screen brightness"),
            ("shell settings put system screen_brightness 200", "Set screen brightness"),
            ("shell am startservice", "Start a service"),
            ("shell am stopservice", "Stop a service"),
            ("shell wm size", "Get screen size"),
            ("shell wm density", "Get screen density"),
            ("shell dumpsys activity", "Dump activity manager"),
            ("shell dumpsys meminfo", "Dump memory info"),
            ("shell dumpsys cpuinfo", "Dump CPU info"),
            ("shell dumpsys package", "Dump package info"),
            ("shell dumpsys window", "Dump window info"),
            ("shell dumpsys connectivity", "Dump connectivity info"),
            ("shell dumpsys sensorservice", "Dump sensor service info"),
            ("shell dumpsys media.audio_flinger", "Dump audio flinger info"),
            ("shell dumpsys batterystats", "Dump battery stats"),
            ("shell dumpsys location", "Dump location service info"),
            ("shell dumpsys telephony.registry", "Dump telephony registry"),
            ("shell dumpsys batteryinfo", "Dump battery info"),
            ("shell dumpsys power", "Dump power info"),
            ("shell dumpsys alarm", "Dump alarm info"),
            ("shell dumpsys gfxinfo", "Dump graphics info"),
            ("shell dumpsys package-usage", "Dump package usage"),
            ("shell dumpsys bluetooth_manager", "Dump Bluetooth manager info"),
            ("shell dumpsys activity service", "Dump activity service info"),
            ("shell dumpsys audio", "Dump audio info"),
            ("shell dumpsys surfaceflinger", "Dump surface flinger info"),
            ("shell dumpsys diskstats", "Dump disk stats"),
            ("shell dumpsys usb", "Dump USB info"),
            ("shell dumpsys display", "Dump display info"),
            ("shell dumpsys notification", "Dump notification info"),
            ("shell dumpsys media_router", "Dump media router info"),
            ("shell dumpsys network_stats", "Dump network stats"),
            ("shell dumpsys dropbox", "Dump dropbox info"),
            ("shell dumpsys media_media_session", "Dump media session info"),
            ("shell dumpsys user_manager", "Dump user manager info"),
            ("shell dumpsys power_usage", "Dump power usage"),
            ("shell dumpsys storage", "Dump storage info"),
            ("shell dumpsys statusbar", "Dump status bar info"),
            ("shell dumpsys activity_manager", "Dump activity manager info"),
            ("shell dumpsys gpuinfo", "Dump GPU info"),
            ("shell dumpsys screen_pinning", "Dump screen pinning info"),
            ("shell dumpsys appops", "Dump app ops info"),
            ("shell dumpsys launcher", "Dump launcher info"),
            ("shell dumpsys accessibility", "Dump accessibility info")
        ]
        self.command_var = ctk.StringVar()
        self.command_dropdown = ctk.CTkComboBox(self.command_frame, variable=self.command_var, values=[cmd[0] for cmd in self.all_commands])
        self.command_dropdown.pack(side="left", padx=10)

        self.execute_dropdown_button = ctk.CTkButton(self.command_frame, text="Execute Selected Command", command=self.execute_selected_command)
        self.execute_dropdown_button.pack(side="left", padx=10)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.command_frame, text="Clear", command=self.clear_output)
        self.clear_button.pack(side="right", padx=10)

        # Cheatsheet Button
        self.cheatsheet_button = ctk.CTkButton(self.command_frame, text="ADB Cheatsheet", command=self.show_cheatsheet)
        self.cheatsheet_button.pack(side="right", padx=10)

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
        if command:
            output = self.run_adb_command(command)
            self.output_text.delete('1.0', ctk.END)
            self.output_text.insert(ctk.END, output)
            self.output_text.yview(ctk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a command.")

    def execute_selected_command(self):
        selected_command = self.command_var.get()
        for cmd, desc in self.all_commands:
            if selected_command == cmd:
                output = self.run_adb_command(cmd)
                self.output_text.delete('1.0', ctk.END)
                self.output_text.insert(ctk.END, output)
                self.output_text.yview(ctk.END)
                return
        messagebox.showwarning("Warning", "Selected command not found.")

    def clear_output(self):
        self.output_text.delete('1.0', ctk.END)

    def show_cheatsheet(self):
        cheatsheet_window = Toplevel(self)
        cheatsheet_window.title("ADB Cheatsheet")

        Label(cheatsheet_window, text="ADB Command Cheatsheet", font=("Arial", 16)).pack(pady=10)

        for cmd, desc in self.all_commands:
            frame = ctk.CTkFrame(cheatsheet_window)
            frame.pack(pady=5, padx=10, fill="x")
            
            cmd_label = ctk.CTkLabel(frame, text=cmd, font=("Arial", 12), anchor="w")
            cmd_label.pack(side="left", padx=10, fill="x")
            
            desc_label = ctk.CTkLabel(frame, text=desc, font=("Arial", 12), anchor="w")
            desc_label.pack(side="left", padx=10, fill="x")

            copy_button = ctk.CTkButton(frame, text="Copy", command=lambda c=cmd: self.copy_to_clipboard(c))
            copy_button.pack(side="right", padx=10)

    def copy_to_clipboard(self, command):
        pyperclip.copy(command)
        messagebox.showinfo("Copied", f"Command '{command}' copied to clipboard.")

    def show_realtime_logcat(self):
        self.run_in_thread(self.realtime_logcat_thread)

    def realtime_logcat_thread(self):
        process = subprocess.Popen([self.adb_path, 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.logcat_process = process
        while not self.stop_logcat:
            line = process.stdout.readline()
            if line:
                self.output_text.insert(ctk.END, line)
                self.output_text.yview(ctk.END)
        process.terminate()

    def stop_realtime_logcat(self):
        self.stop_logcat = True
        if hasattr(self, 'logcat_process'):
            self.logcat_process.terminate()

    def capture_screenshot(self):
        self.run_in_thread(self.capture_screenshot_thread)

    def capture_screenshot_thread(self):
        output = self.run_adb_command('shell screencap -p /sdcard/screenshot.png')
        if "error" in output.lower():
            messagebox.showerror("Error", "Failed to capture screenshot.")
            return

        self.run_adb_command('pull /sdcard/screenshot.png .')
        self.run_adb_command('shell rm /sdcard/screenshot.png')
        messagebox.showinfo("Screenshot", "Screenshot saved to current directory.")

    def reboot_device(self):
        self.run_in_thread(self.reboot_device_thread)

    def reboot_device_thread(self):
        output = self.run_adb_command('reboot')
        messagebox.showinfo("Reboot Device", output)

    def save_logs_as_csv(self):
        output = self.run_adb_command('logcat -d')
        if not output:
            messagebox.showerror("Error", "Failed to retrieve logs.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Logcat Output"])
                for line in output.splitlines():
                    writer.writerow([line])
            messagebox.showinfo("Save Logs", "Logs saved successfully.")

    def pull_file(self):
        # Placeholder method
        pass

    def push_file(self):
        # Placeholder method
        pass

    def run_in_thread(self, target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.start()

    def on_closing(self):
        self.stop_realtime_logcat()
        self.destroy()

if __name__ == "__main__":
    app = ADBGuiApp()
    app.mainloop()

