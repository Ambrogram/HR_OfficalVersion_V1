from mysql.connector import Error
from tkinter import messagebox
from .db_connection import connect_db

def initialize_db():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Create Participants table with updated schema
            cur.execute('''CREATE TABLE IF NOT EXISTS Participants (
                                ParticipantID INT AUTO_INCREMENT PRIMARY KEY,
                                FirstName VARCHAR(255) NOT NULL,
                                LastName VARCHAR(255),
                                Age INT,
                                Gender ENUM('Male', 'Female', 'Other'),
                                Education ENUM('-- select one --', 'No formal education', 'Primary education', 
                                                'Secondary education or high school', 'GED', 'Vocational qualification', 
                                                'Bachelor''s degree', 'Master''s degree', 'Doctorate or higher'),
                                Occupation ENUM('Pilots', 'Race Car Drivers', 'Video Game Testers', 'Professional Gamers', 
                                                'Paramedics', 'Firefighters', 'Police Officers', 'Military Personnel', 
                                                'Sprinters', 'Soccer Players', 'none of the above'),
                                Colorblind BOOLEAN,
                                MedicalHistory ENUM('Neurological Disorders', 'Mental Health Issues', 'Substance Abuse Disorders',
                                                    'Sleep Disorders', 'Chronic Fatigue Syndrome', 'none of the above')
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
            
            # Create Settings table
            cur.execute('''CREATE TABLE IF NOT EXISTS Settings (
                                SettingID INT AUTO_INCREMENT PRIMARY KEY,
                                ParticipantID INT,
                                FrequencyRange ENUM('1', '2', '3'),
                                NumberOfEvents ENUM('33', '66', '99', '102', '120', '150', '180', '201', '306'),
                                FOREIGN KEY (ParticipantID) REFERENCES Participants(ParticipantID)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
            
            # Create Tests table with updated schema
            cur.execute('''CREATE TABLE IF NOT EXISTS Tests (
                                TestID INT AUTO_INCREMENT PRIMARY KEY,
                                ParticipantID INT,
                                SettingID INT,
                                TestDate DATETIME,
                                CorrectAnswers INT,  -- Correct answers now comes before CorrectRate and TotalTimeCost
                                CorrectRate FLOAT,
                                TotalTimeCost FLOAT,
                                FOREIGN KEY (ParticipantID) REFERENCES Participants(ParticipantID),
                                FOREIGN KEY (SettingID) REFERENCES Settings(SettingID)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
            
            # Create Statistics table (optional)
            cur.execute('''CREATE TABLE IF NOT EXISTS Statistics (
                                StatisticID INT AUTO_INCREMENT PRIMARY KEY,
                                TestID INT,
                                AverageReactionTime FLOAT,
                                CorrectnessRate FLOAT,
                                FOREIGN KEY (TestID) REFERENCES Tests(TestID)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')

            conn.commit()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
        finally:
            cur.close()
            conn.close()

def insert_participant(participant_info):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO Participants 
                              (FirstName, LastName, Age, Gender, Education, Occupation, Colorblind, MedicalHistory) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (participant_info['FirstName'], participant_info['LastName'], participant_info['Age'],
                            participant_info['Gender'], participant_info['Education'], participant_info['Occupation'],
                            participant_info['ColorBlind'] == "Yes", participant_info['MedicalHistory']))
            conn.commit()
            participant_id = cursor.lastrowid  # Get the inserted participant's ID
            return participant_id
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to save participant: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return None

def insert_settings(participant_id, settings):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            colors_str = ','.join(settings['colors'])  # Convert the list of colors to a comma-separated string
            cursor.execute('''INSERT INTO Settings 
                              (ParticipantID, FrequencyRange, NumberOfEvents, Colors) 
                              VALUES (%s, %s, %s, %s)''', 
                           (participant_id, str(settings['frequency'][1]), str(settings['events']), colors_str))
            conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to save settings: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return False
