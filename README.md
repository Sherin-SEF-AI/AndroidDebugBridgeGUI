# AndroidDebugBridgeGUI
python application for Android Debugging

# ADB GUI Tool

## Overview

The **ADB GUI Tool** is a graphical interface for interacting with Android Debug Bridge (ADB) commands. This tool allows users to execute ADB commands, manage files between a host and Android devices, capture screenshots, view real-time logcat output, and more—all through a user-friendly GUI built with Python and the CustomTkinter library.

## Features

- **Device Management**: List and view connected Android devices.
- **Command Execution**: Execute various ADB commands and view their output.
- **Command Dropdown**: Quick access to a wide range of predefined ADB commands.
- **File Operations**: Push and pull files between the host and Android device.
- **Real-time Logcat**: View real-time logcat output with the ability to stop the logcat process.
- **Screenshot Capture**: Capture and save screenshots from the Android device.
- **Log Export**: Save command outputs and logcat data as CSV files.
- **Cheatsheet**: Access a comprehensive cheatsheet of ADB commands.

## Requirements

- Python 3.x
- CustomTkinter (`pip install customtkinter`)
- Pyperclip (`pip install pyperclip`)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AndroidDebugBridgeGUI.git
    cd AndroidDebugBridgeGUI
    ```

2. **Install Dependencies**:
    ```bash
    pip install customtkinter pyperclip
    ```

3. **Ensure ADB is Installed**: Make sure ADB is installed and accessible from your command line. You can download ADB as part of the Android SDK Platform Tools from [Android Developer](https://developer.android.com/studio/releases/platform-tools).

## Usage

1. **Run the Application**:
    ```bash
    python adb_gui_tool.py
    ```

2. **Main Features**:
    - **Update Device List**: Click the "Update Device List" button to view connected devices.
    - **Execute Command**: Enter any ADB command in the input field and click "Execute Command" to run it.
    - **Dropdown Commands**: Select a command from the dropdown menu and click "Execute Selected Command" to run it.
    - **File Operations**: Use the "Push File" and "Pull File" buttons to transfer files between the host and device.
    - **Real-time Logcat**: Click "Show Real-time Logcat" to start viewing logcat data. Click "Stop Logcat" to stop it.
    - **Capture Screenshot**: Click "Capture Screenshot" to take a screenshot and save it.
    - **Save Logs as CSV**: Click "Save Logs as CSV" to export command outputs and logcat data.
    - **Cheatsheet**: Click "ADB Cheatsheet" to open a window with a list of common ADB commands.

## Example

To view the connected devices and execute a command:

1. Click "Update Device List" to display connected devices.
2. Enter an ADB command in the command input field.
3. Click "Execute Command" to run the command and view the output in the textbox.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [your.email@example.com](mailto:testingdebug22@gmail.com).
Created By Sherin Joseph Roy
---

Enjoy using the ADB GUI Tool! Feel free to contribute or customize it according to your needs.

