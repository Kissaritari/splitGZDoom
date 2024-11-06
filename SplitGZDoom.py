import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import time
import os
import json

# Config file path
CONFIG_FILE = "gzdoom_config.json"

# Define difficulty levels for GZDoom
difficulty_levels = {
    "I'm Too Young To Die": "0",
    "Hey, Not Too Rough": "1",
    "Hurt Me Plenty": "2",
    "Ultra-Violence": "3",
    "Nightmare!": "4"
}




# Function to load configuration from the config file
def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            host_path_var.set(config.get("host_path", ""))
            client_path_var.set(config.get("client_path", ""))
            iwad_path_var.set(config.get("iwad_path", ""))
            wad_paths_var.set(config.get("wad_paths", ""))
    else:
        # If config file does not exist, set defaults
        host_path_var.set("")
        client_path_var.set("")
        iwad_path_var.set("")
        wad_paths_var.set("")

# Function to save configuration to the config file
def save_config():
    config = {
        "host_path": host_path_var.get(),
        "client_path": client_path_var.get(),
        "iwad_path": iwad_path_var.get(),
        "wad_paths": wad_paths_var.get(),
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

# Function to launch GZDoom instances
# Modify the launch function to include difficulty
def launch_gzdoom():
    # Get the file paths and settings from the GUI
    gzdoom_host = host_path_var.get()
    gzdoom_client = client_path_var.get()
    iwad_file = iwad_path_var.get()
    wad_files = wad_paths_var.get()
    difficulty = difficulty_levels[difficulty_var.get()]

    # Validate inputs
    if not os.path.isfile(gzdoom_host):
        messagebox.showerror("Error", "Invalid host GZDoom path.")
        return
    if not os.path.isfile(gzdoom_client):
        messagebox.showerror("Error", "Invalid client GZDoom path.")
        return
    if not os.path.isfile(iwad_file):
        messagebox.showerror("Error", "Invalid IWAD file path.")
        return

    # Save configuration
    save_config()

    # Split WAD files if multiple paths are entered
    wad_files_list = wad_files.split() if wad_files else []

    # Launch host with difficulty setting
    host_command = [gzdoom_host, '-host', '2', '-iwad', iwad_file, '-skill', difficulty] + wad_files_list
    subprocess.Popen(host_command)
    
    # Wait briefly to ensure host is ready
    time.sleep(2)
    
    # Launch client with difficulty setting
    client_command = [gzdoom_client, '-join', 'localhost', '-iwad', iwad_file, '-skill', difficulty] + wad_files_list
    subprocess.Popen(client_command)

# File selection functions
def select_host_path():
    path = filedialog.askopenfilename(title="Select Host GZDoom Executable", filetypes=[("Exe files", "*.exe")])
    host_path_var.set(path)

def select_client_path():
    path = filedialog.askopenfilename(title="Select Client GZDoom Executable", filetypes=[("Exe files", "*.exe")])
    client_path_var.set(path)

def select_iwad():
    path = filedialog.askopenfilename(title="Select IWAD File", filetypes=[("WAD files", "*.wad")])
    iwad_path_var.set(path)

def select_wad_files():
    paths = filedialog.askopenfilenames(title="Select WAD File(s)")
    wad_paths_var.set(" ".join(paths))

# Initialize the main window
root = tk.Tk()
root.title("GZDoom Multiplayer Launcher")

# Variables for storing file paths
host_path_var = tk.StringVar()
client_path_var = tk.StringVar()
iwad_path_var = tk.StringVar()
wad_paths_var = tk.StringVar()

# Load the last configuration
load_config()

# Host path selection
tk.Label(root, text="Host GZDoom Path:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=host_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse...", command=select_host_path).grid(row=0, column=2)

# Client path selection
tk.Label(root, text="Client GZDoom Path:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=client_path_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse...", command=select_client_path).grid(row=1, column=2)

# IWAD file selection
tk.Label(root, text="IWAD File:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=iwad_path_var, width=50).grid(row=2, column=1)
tk.Button(root, text="Browse...", command=select_iwad).grid(row=2, column=2)

# Optional WAD files selection
tk.Label(root, text="Optional WAD File(s):").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=wad_paths_var, width=50).grid(row=3, column=1)
tk.Button(root, text="Browse...", command=select_wad_files).grid(row=3, column=2)

# Variable to store the selected difficulty level
difficulty_var = tk.StringVar(value="Hurt Me Plenty")  # Default difficulty

# Difficulty level selection
tk.Label(root, text="Difficulty Level:").grid(row=4, column=0, sticky="e")
difficulty_menu = tk.OptionMenu(root, difficulty_var, *difficulty_levels.keys())
difficulty_menu.grid(row=4, column=1)

# Launch button
tk.Button(root, text="Launch Multiplayer", command=launch_gzdoom).grid(row=4, column=0, columnspan=3, pady=10)

# Run the Tkinter main loop
root.mainloop()
