import tkinter as tk
from tkinter import ttk, messagebox
from database.db_operations import insert_participant
from settings.settings_manager import SettingsManager

class ResearcherWindow:
    def __init__(self, root, app):
        self.root = tk.Toplevel(root)
        self.root.title("Researcher Window")
        self.root.geometry("500x450")
        self.app = app
        
        self.root.configure(bg='#2d2d2d')
        
        self.settings_manager = None

        # Add settings icon and title
        settings_icon = ttk.Button(self.root, text="⚙️ Settings", command=self.open_settings)
        settings_icon.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        title_label = ttk.Label(self.root, text="Participant Information", font=("Helvetica", 16, "bold"), background='#2d2d2d', foreground='white')
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Participant Information Form
        self.create_form()

    def create_form(self):
        ttk.Label(self.root, text="First Name:", background='#2d2d2d', foreground='white').grid(row=1, column=0, pady=10, padx=20, sticky=tk.W)
        self.first_name_entry = ttk.Entry(self.root)
        self.first_name_entry.grid(row=1, column=1, pady=10, padx=20, sticky=tk.EW)

        ttk.Label(self.root, text="Last Name:", background='#2d2d2d', foreground='white').grid(row=2, column=0, pady=10, padx=20, sticky=tk.W)
        self.last_name_entry = ttk.Entry(self.root)
        self.last_name_entry.grid(row=2, column=1, pady=10, padx=20, sticky=tk.EW)

        # Age
        ttk.Label(self.root, text="Age:", background='#2d2d2d', foreground='white').grid(row=3, column=0, pady=10, padx=20, sticky=tk.W)
        self.age_entry = ttk.Entry(self.root)
        self.age_entry.grid(row=3, column=1, pady=10, padx=20, sticky=tk.EW)

        # Gender
        ttk.Label(self.root, text="Gender:", background='#2d2d2d', foreground='white').grid(row=4, column=0, pady=10, padx=20, sticky=tk.W)
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.root, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly")
        self.gender_combobox.grid(row=4, column=1, pady=10, padx=20, sticky=tk.EW)

        # Education
        self.education_var = tk.StringVar()
        self.education_combobox = ttk.Combobox(self.root, textvariable=self.education_var, 
                                        values=["-- select one --", "No formal education", "Primary education", 
                                                "Secondary education or high school", "GED", "Vocational qualification", 
                                                "Bachelor's degree", "Master's degree", "Doctorate or higher"], state="readonly")
        self.education_combobox.set("-- select one --")  # Default value
        ttk.Label(self.root, text="Education:", background='#2d2d2d', foreground='white').grid(row=5, column=0, pady=10, padx=20, sticky=tk.W)
        self.education_combobox.grid(row=5, column=1, pady=10, padx=20, sticky=tk.EW)

        # Occupation
        occupation_options = ["Pilots", "Race Car Drivers", "Video Game Testers", "Professional Gamers",
                            "Paramedics", "Firefighters", "Police Officers", "Military Personnel",
                            "Sprinters", "Soccer Players", "none of the above"]

        self.occupation_var = tk.StringVar()
        self.occupation_combobox = ttk.Combobox(self.root, textvariable=self.occupation_var, values=occupation_options, state="readonly")
        self.occupation_combobox.set("none of the above")  # Default value
        ttk.Label(self.root, text="Occupation:", background='#2d2d2d', foreground='white').grid(row=6, column=0, pady=10, padx=20, sticky=tk.W)
        self.occupation_combobox.grid(row=6, column=1, pady=10, padx=20, sticky=tk.EW)

        # Color Blind
        ttk.Label(self.root, text="Color Blind:", background='#2d2d2d', foreground='white').grid(row=7, column=0, pady=10, padx=20, sticky=tk.W)
        self.color_blind_var = tk.StringVar()
        self.color_blind_combobox = ttk.Combobox(self.root, textvariable=self.color_blind_var, values=["Yes", "No"], state="readonly")
        self.color_blind_combobox.grid(row=7, column=1, pady=10, padx=20, sticky=tk.EW)

        # Medical History
        medical_history_options = ["Neurological Disorders", "Mental Health Issues", "Substance Abuse Disorders",
                                "Sleep Disorders", "Chronic Fatigue Syndrome", "none of the above"]

        self.medical_history_var = tk.StringVar()
        self.medical_history_combobox = ttk.Combobox(self.root, textvariable=self.medical_history_var, values=medical_history_options, state="readonly")
        self.medical_history_combobox.set("none of the above")  # Default value
        ttk.Label(self.root, text="Medical History:", background='#2d2d2d', foreground='white').grid(row=8, column=0, pady=10, padx=20, sticky=tk.W)
        self.medical_history_combobox.grid(row=8, column=1, pady=10, padx=20, sticky=tk.EW)

        # Save button
        save_button = ttk.Button(self.root, text="Save Participant", command=self.save_participant)
        save_button.grid(row=9, column=0, columnspan=2, pady=20)

    def save_participant(self):
        participant_info = {
            'FirstName': self.first_name_entry.get(),
            'LastName': self.last_name_entry.get(),
            'Age': self.age_entry.get(),
            'Gender': self.gender_var.get(),
            'Education': self.education_combobox.get(),
            'Occupation': self.occupation_combobox.get(),
            'ColorBlind': self.color_blind_var.get(),
            'MedicalHistory': self.medical_history_var.get()
        }

        # Save participant info to the database
        participant_id = insert_participant(participant_info)
        if insert_participant(participant_info):
            self.app.participant_id = participant_id  # Save the participant_id in the app context
            messagebox.showinfo("Success", "Participant saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to save participant.")

    def open_settings(self):
        if self.settings_manager is None or not self.settings_manager.root.winfo_exists():
            self.settings_manager = SettingsManager(self.root, self)
        else:
            self.settings_manager.root.lift()

    def set_settings(self, settings):
        self.app.settings = settings  # Store selected settings in the shared attribute
