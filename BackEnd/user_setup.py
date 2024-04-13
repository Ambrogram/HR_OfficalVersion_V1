import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import mysql.connector
import subprocess
import os
import json
import sys


# GUI setup
root = ThemedTk(theme="equilux")  # Equilux theme has a darker, more modern aesthetic
root.title("User Setup for Reaction Time Test")
root.geometry("500x360")

# Function to connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="humanreaction.mysql.database.azure.com",
        port=3306,
        user="Ambrose",
        password="NEUyang7034",
        database="human_reaction"
    )

# Function to initialize the database tables
def initialize_db():
    conn = connect_db()
    cur = conn.cursor()
    
    # Create Participants table
    cur.execute('''CREATE TABLE IF NOT EXISTS Participants (
                        ParticipantID INT AUTO_INCREMENT PRIMARY KEY,
                        FirstName VARCHAR(255) NOT NULL,
                        LastName VARCHAR(255) NOT NULL,
                        Age INT,
                        Gender ENUM('Male', 'Female', 'Other'),
                        Education VARCHAR(255),
                        Occupation VARCHAR(255),
                        Colorblind BOOLEAN,
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
    
    # Create Tests table
    cur.execute('''CREATE TABLE IF NOT EXISTS Tests (
                        TestID INT AUTO_INCREMENT PRIMARY KEY,
                        ParticipantID INT,
                        TestLevel ENUM('A', 'B', 'C', 'D'),
                        FOREIGN KEY (ParticipantID) REFERENCES Participants(ParticipantID)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
    
    # Create Events table
    cur.execute('''CREATE TABLE IF NOT EXISTS Events (
                        EventID INT AUTO_INCREMENT PRIMARY KEY,
                        TestID INT,
                        ReactionTime FLOAT,
                        FOREIGN KEY (TestID) REFERENCES Tests(TestID)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')

    conn.commit()
    conn.close()
    

freq_var = tk.StringVar()
events_var = tk.StringVar()
    
def settings_window():
    # New Window for setting the frequency range and number of events
    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("300x200")
    
    # Frequency Range Setting
    ttk.Label(win, text="Set Frequency Range:").pack(pady=10)
    frequency_options = ["1", "2", "3"]
    global freq_var
    freq_var = tk.StringVar(win)
    freq_dropdown = ttk.Combobox(win, textvariable=freq_var, values=frequency_options, state="readonly")
    freq_dropdown.pack(pady=5)

    # Number of Events Setting
    ttk.Label(win, text="Set Number of Events:").pack(pady=10)
    event_options = ["33", "66", "99", "102", "120", "150", "180", "201", "306"]
    global events_var  # Declare as global
    events_var.set("102")  # Default setting
    events_var = tk.StringVar()
    events_dropdown = ttk.Combobox(win, textvariable=events_var, values=event_options, state="readonly")
    events_dropdown.pack(pady=5)
    
    
    # Save Settings Button
    save_settings_btn = ttk.Button(win, text="Save Settings", command=lambda: save_settings(freq_var.get(), events_var.get()))
    save_settings_btn.pack(pady=20)

def save_settings(freq_range, events_count):
    # Function to save the settings from the settings window
    print("Frequency Range Set To:", freq_range)
    print("Number of Events Set To:", events_count)
    messagebox.showinfo("Settings Saved", f"Frequency: {freq_range} sec, Events: {events_count}")
    # You might want to save these settings to a file or database

def save_user_settings():
    user_info = {
        "FirstName": name_entry.get().strip(),
        #"LastName": "",
        "Age": age_entry.get(),
        "Gender": gender_combobox.get(),
        "Education": education_combobox.get().replace("'", "''"),  # Escaping single quotes
        "Occupation": occupation_combobox.get(),
        "Colorblind": 1 if color_blind_combobox.get() == "Yes" else 0,
        #"EventsCount": events_count_combobox.get()
    }
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO Participants 
                          (FirstName, LastName, Age, Gender, Education, Occupation, Colorblind) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                       (user_info['FirstName'], '', user_info['Age'], user_info['Gender'],
                        user_info['Education'], user_info['Occupation'], user_info['Colorblind']))
        conn.commit()
        messagebox.showinfo("Success", "User settings saved successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        messagebox.showerror("Database Error", f"Failed to save user settings: {e}")
    finally:
        conn.close()
        
        
        

def save_and_launch_test(events_count, frequency_range):
    events_count = events_var.get()
    # Multiply by 1000 to convert seconds to milliseconds for the frequency range
    frequency_range = str(int(freq_var.get()) * 1000) if freq_var.get().isdigit() else "1000"
    # Debugging output
    print("Debug - Events Count:", events_count)
    print("Debug - Frequency Range:", frequency_range)
    
    if not events_count.isdigit():  # Validation to check if events_count is a digit
        messagebox.showerror("Error", "Invalid number of events. Please enter a valid integer.")
        return  # Stop execution if the validation fails

    
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Absolute path of the directory of the current script
    script_path = os.path.join(script_directory, 'test.py')  # Path to the test.py script

    # Build command with properly formatted arguments
    command = [
        sys.executable,
        script_path,
        f"--eventsCount={events_count}",
        f"--frequencyRange={frequency_range}"
    ]
    print("Debug - Command:", command)  # Print the full command for debugging
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.showinfo("Success", "Test launched successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.stdout.decode()}")  # Decode the output to make it readable
        print(f"Error: {e.stderr.decode()}")  # Decode the stderr to make it readable
        messagebox.showerror("Launch Error", f"Failed to launch the test: {e}")
    except Exception as ex:
        messagebox.showerror("Unexpected Error", str(ex))

# Usage example (ensure these values are defined)
events_var.set("102")  # Ensuring it has a default valid value
freq_var.set("2")  # Default frequency in seconds
#save_and_launch_test("33", "2000")

# Example usage with static values for debugging
#launch_test_script(33, 2000)  # Ensure these are not empty and correctly formatted
"""
def setup_call():
    # This could be linked to a button press or some other event
    events_count = events_var.get()  # Assuming these are Tkinter StringVar() or similar
    frequency_range = freq_var.get().strip(' seconds')
    save_and_launch_test(events_count, frequency_range)  # Correctly pass parameters
"""
    


# Creating form fields
# Creating form fields


# Enhance the default font for a more futuristic look
default_font = ("Helvetica", 10, "bold")
root.option_add("*Font", default_font)
root.option_add("*Foreground", "#00FF00")  # Green text, common in sci-fi themes
root.option_add("*Background", "#000000")  # Black background
root.configure(background="#000000")

style = ttk.Style(root)
style.configure('TLabel', background="#000000", foreground="#00FF00")
style.configure('TEntry', fieldbackground="#222222", foreground="#00FF00")
style.configure('TButton', background="#222222", foreground="#00FF00", borderwidth=1)
style.configure('TCombobox', fieldbackground="#222222", foreground="#00FF00", selectbackground="#333333", selectforeground="#00FF00")
style.map('TCombobox', fieldbackground=[('readonly', '#222222')], selectbackground=[('readonly', '#333333')], selectforeground=[('readonly', '#00FF00')])
style.configure('Horizontal.TProgressbar', background='#00FF00')


# Adding settings icon and title
settings_icon = ttk.Button(root, text="⚙️", command=settings_window, style='TButton')
settings_icon.place(x=460, y=10)

title_label = ttk.Label(root, text="Participant Information Entry", font=("Helvetica", 14, "bold"), background="#333", foreground="#FFF")
title_label.grid(row=2, column=0, columnspan=2, pady=20, padx=10)


# Name
ttk.Label(root, text="Name:").grid(row=4, column=0, pady=10, padx=20, sticky=tk.W)
name_entry = ttk.Entry(root)
name_entry.grid(row=4, column=1, pady=10, padx=20, sticky=tk.EW)

# Age
ttk.Label(root, text="Age:").grid(row=5, column=0, pady=10, padx=20, sticky=tk.W)
age_entry = ttk.Entry(root)
age_entry.grid(row=5, column=1, pady=10, padx=20, sticky=tk.EW)

# Gender
ttk.Label(root, text="Gender:").grid(row=6, column=0, pady=10, padx=20, sticky=tk.W)
gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly")
gender_combobox.grid(row=6, column=1, pady=10, padx=20, sticky=tk.EW)

# Education
education_var = tk.StringVar()
education_combobox = ttk.Combobox(root, textvariable=education_var, 
                                   values=["-- select one --", "No formal education", "Primary education", 
                                           "Secondary education or high school", "GED", "Vocational qualification", 
                                           "Bachelor's degree", "Master's degree", "Doctorate or higher"], state="readonly")
education_combobox.set("-- select one --")  # Default value
ttk.Label(root, text="Education:").grid(row=7, column=0, pady=10, padx=20, sticky=tk.W)
education_combobox.grid(row=7, column=1, pady=10, padx=20, sticky=tk.EW)


# Occupation Dropdown
occupation_options = ["Pilots", "Race Car Drivers", "Video Game Testers", "Professional Gamers",
                      "Paramedics", "Firefighters", "Police Officers", "Military Personnel",
                      "Sprinters", "Soccer Players", "none of the above"]

occupation_var = tk.StringVar()
occupation_combobox = ttk.Combobox(root, textvariable=occupation_var, values=occupation_options, state="readonly")
occupation_combobox.set("none of the above")  # Default value
ttk.Label(root, text="Occupation:").grid(row=8, column=0, pady=10, padx=20, sticky=tk.W)
occupation_combobox.grid(row=8, column=1, pady=10, padx=20, sticky=tk.EW)


# Color Blind
ttk.Label(root, text="Color Blind:").grid(row=9, column=0, pady=10, padx=20, sticky=tk.W)
color_blind_var = tk.StringVar()
color_blind_combobox = ttk.Combobox(root, textvariable=color_blind_var, values=["Yes", "No"], state="readonly")
color_blind_combobox.grid(row=9, column=1, pady=10, padx=20, sticky=tk.EW)

# Medical History Dropdown
medical_history_options = ["Neurological Disorders", "Mental Health Issues", "Substance Abuse Disorders",
                           "Sleep Disorders", "Chronic Fatigue Syndrome", "none of the above"]

medical_history_var = tk.StringVar()
medical_history_combobox = ttk.Combobox(root, textvariable=medical_history_var, values=medical_history_options, state="readonly")
medical_history_combobox.set("none of the above")  # Default value
ttk.Label(root, text="Medical History:").grid(row=10, column=0, pady=10, padx=20, sticky=tk.W)
medical_history_combobox.grid(row=10, column=1, pady=10, padx=20, sticky=tk.EW)



# Test Level
#ttk.Label(root, text="Test Level (A/B/C/D):").grid(row=6, column=0, pady=10, sticky=tk.W)
#level_var = tk.StringVar()
#level_combobox = ttk.Combobox(root, textvariable=level_var, values=["A", "B", "C", "D"], state="readonly")
#level_combobox.grid(row=6, column=1, pady=10, sticky=tk.EW)

"""
# Test Events Count
ttk.Label(root, text="Number of Events:").grid(row=11, column=0, pady=10, sticky=tk.W)
events_count_var = tk.StringVar()
events_count_combobox = ttk.Combobox(root, textvariable=events_count_var, values=["102","33", "66", "99", "204", "306"], state="readonly")
events_count_combobox.grid(row=11, column=1, pady=10, sticky=tk.EW)


# Input Method
ttk.Label(root, text="Input Method:").grid(row=10, column=0, pady=10, sticky=tk.W)
input_method_var = tk.StringVar()
input_method_combobox = ttk.Combobox(root, textvariable=input_method_var, values=["buttons", "keyboard"], state="readonly")
input_method_combobox.grid(row=10, column=1, pady=10, sticky=tk.EW)
"""



# Save button
ttk.Label(root, text="").grid(row=8, column=0) # Spacer
save_button = ttk.Button(root, text="Save and Start Test", command=lambda: save_and_launch_test(events_var.get(), str(int(freq_var.get()) * 1000)))
save_button.grid(row=12, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=10)
root.columnconfigure(1, weight=1)

root.mainloop()
