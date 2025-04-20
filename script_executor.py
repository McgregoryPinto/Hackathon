import tkinter as tk
from tkinter import filedialog
import subprocess

# Function to execute the selected script
def execute_script(script_name, video_path=None):
    command = ['python3', script_name]
    if video_path:
        command.append(video_path)
    subprocess.run(command)

# Function to open file dialog
def open_file_dialog():
    return filedialog.askopenfilename(title="Select a Video File", filetypes=[("Video Files", "*.mp4 *.avi")])

# Function to handle script selection and execution
def run_selected_script():
    script = script_var.get()
    use_video = video_var.get()
    video_path = open_file_dialog() if use_video else None
    execute_script(script, video_path)

# Create the main window
root = tk.Tk()
root.title("Script Executor")

# Script selection
script_var = tk.StringVar(value='pred_local_captura_webcam.py')
script_label = tk.Label(root, text="Select Script:")
script_label.pack()
script_options = ["pred_local_captura_webcam.py", "pred_yolo_captura_webcam.py"]
script_menu = tk.OptionMenu(root, script_var, *script_options)
script_menu.pack()

# Video or Webcam selection
video_var = tk.BooleanVar()
video_check = tk.Checkbutton(root, text="Use Video File", variable=video_var)
video_check.pack()

# Run button
run_button = tk.Button(root, text="Run", command=run_selected_script)
run_button.pack()

# Start the GUI event loop
root.mainloop()