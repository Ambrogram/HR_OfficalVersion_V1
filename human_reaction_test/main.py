from ttkthemes import ThemedTk
from tkinter import ttk
from gui.researcher_window import ResearcherWindow
from gui.participant_window import ParticipantWindow

class App:
    def __init__(self, root):
        self.root = root
        self.settings = None  # Shared attribute to store settings
        self.participant_id = None  # Attribute to store the participant ID
        
        # Set window background color
        self.root.configure(bg='#2d2d2d')
        
        # Welcome message
        welcome_label = ttk.Label(root, text="WELCOME", font=("Helvetica", 24, "bold"))
        welcome_label.pack(pady=(100, 20))

        # Researcher button
        researcher_button = ttk.Button(root, text="Researcher", command=self.open_researcher_window)
        researcher_button.pack(ipadx=10, ipady=5, pady=10)

        # Participant button
        participant_button = ttk.Button(root, text="Participants", command=self.open_participant_window)
        participant_button.pack(ipadx=10, ipady=5, pady=10)

    def open_researcher_window(self):
        researcher_window = ResearcherWindow(self.root, self)

    def open_participant_window(self):
        participant_window = ParticipantWindow(self.root, self)

def main():
    root = ThemedTk(theme="equilux")
    root.title("Welcome to the Reaction Time Test")
    root.geometry("600x400")

    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
