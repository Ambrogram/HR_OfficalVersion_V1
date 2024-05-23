import tkinter as tk
from tkinter import ttk, messagebox
from database.db_operations import insert_settings

class SettingsManager:
    def __init__(self, parent, researcher_window):
        self.root = tk.Toplevel(parent)
        self.root.title("Settings")
        self.root.geometry("300x200")
        self.researcher_window = researcher_window # Reference to the ResearcherWindow

        self.root.configure(bg='#2d2d2d')
        
        # Generate settings
        self.settings = self.generate_settings()
        self.setting_var = tk.StringVar(self.root)

        ttk.Label(self.root, text="Select Setting ID:").pack(pady=10)
        setting_ids = [str(setting['settingID']) for setting in self.settings]
        setting_dropdown = ttk.Combobox(self.root, textvariable=self.setting_var, values=setting_ids, state="readonly")
        setting_dropdown.pack(pady=5)

        save_settings_btn = ttk.Button(self.root, text="Save Settings", command=self.save_settings)
        save_settings_btn.pack(pady=20)

    def generate_settings(self):
        color_levels = {
            1: ['Red', 'Green', 'Blue'],
            2: ['Red', 'Green', 'Blue', 'Yellow', 'White'],
            3: ['Red', 'Green', 'Blue', 'Yellow', 'White', 'Orange', 'Cyan']
        }

        frequency_levels = {
            1: (1, 1),
            2: (1, 2),
            3: (1, 3)
        }

        event_levels = [33, 66, 99]

        settings = []
        setting_id = 1

        for color_level in color_levels:
            for frequency_level in frequency_levels:
                for event_level in event_levels:
                    settings.append({
                        'settingID': setting_id,
                        'colors': color_levels[color_level],
                        'frequency': frequency_levels[frequency_level],
                        'events': event_level
                    })
                    setting_id += 1

        return settings

    def save_settings(self):
        selected_setting_id = int(self.setting_var.get())
        selected_setting = next(setting for setting in self.settings if setting['settingID'] == selected_setting_id)
        
        # Debug log
        print(f"Attempting to save setting: {selected_setting}")

        # Retrieve participant ID
        participant_id = self.researcher_window.app.participant_id  # Assuming participant_id is stored in app context
        
        # Save settings to the database
        # Replace this with the actual participant ID from your application context
        if insert_settings(participant_id, selected_setting):
            messagebox.showinfo("Settings Saved", f"Setting ID: {selected_setting_id} saved")
        else:
            messagebox.showerror("Error", "Failed to save settings")

        # Pass the selected settings to the experiment program
        print(f"Selected Setting: {selected_setting}")
        self.researcher_window.set_settings(selected_setting)  # Store the settings in ResearcherWindow
        
        # Save or pass settings to the main experiment program as needed
        messagebox.showinfo("Settings Saved", f"Setting ID: {selected_setting_id} saved")
    
    def show(self):
        self.root.deiconify()
