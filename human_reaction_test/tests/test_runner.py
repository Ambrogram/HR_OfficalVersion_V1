import tkinter as tk
from tkinter import ttk
import random
import time
import datetime
import mysql.connector
from mysql.connector import Error

class TestRunner:
    def __init__(self, parent, settings):
        self.settings = settings
        
        self.root = tk.Toplevel(parent)
        self.root.title("Reaction Time Test")
        
        self.event_counter = 0
        self.correct_answers = 0
        self.current_color = ''
        self.current_display_color = ''
        self.test_start_time = time.time()
        self.response_recorded = False  # Track if the response for the current event has been recorded
        
        self.colors = self.settings['colors']
        self.color_values = {
            'Red': '#FF0000',
            'Green': '#008000',
            'Blue': '#0000FF',
            'Yellow': '#FFFF00',
            'White': '#FFFFFF',
            'Orange': '#FFA500',
            'Cyan': '#00FFFF'
        }
        self.key_to_color = {
            'r': 'Red',
            'g': 'Green',
            'b': 'Blue',
            'y': 'Yellow',
            'w': 'White',
            'o': 'Orange',
            'c': 'Cyan'
        }
        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()

        self.feedback_label = ttk.Label(self.root, text="", font=('Helvetica', 16), bg='black', fg='white')
        self.feedback_label.pack(pady=10)
        
        self.root.bind("<KeyPress>", self.record_response)
        self.show_stimulus()
        self.root.mainloop()

    def connect_db(self):
        try:
            connection = mysql.connector.connect(
                host="cognitivereaction.mysql.database.azure.com",
                port=3306,
                user="Ambrose",
                password="NEUyang7034",
                database="cognitive_reaction"
            )
            print("Database connected successfully.")
            return connection
        except Error as e:
            print("Failed to connect to database:", e)
            return None

    def insert_test_data(self, correct_answers, correct_rate, total_time_cost):
        print(f"Inserting data: {correct_answers}, {correct_rate}, {total_time_cost}")  # Debug print
        conn = self.connect_db()
        if not conn:
            print("Connection failed")  # Debug print
            return
        cursor = conn.cursor()
        try:
            test_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Date: {test_date}")  # Debug print
            
            cursor.execute('''
                INSERT INTO Tests (ParticipantID, SettingID, TestDate, CorrectAnswers, CorrectRate, TotalTimeCost) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (1, 1, test_date, correct_answers, correct_rate, total_time_cost))
            conn.commit()
            print("Test data saved successfully.")
        except Error as e:
            print("Failed to save test data:", e)
        finally:
            cursor.close()
            conn.close()

    def show_stimulus(self):
        print(f"Event {self.event_counter+1}/{self.settings['events']}")  # Debug print
        self.response_recorded = False  # Reset response recorded flag
        self.level = random.choice(['A', 'B', 'C'])
        self.current_color = random.choice(self.colors)
        if self.level == "C":
            mismatch_colors = [c for c in self.colors if c != self.current_color]
            self.current_display_color = random.choice(mismatch_colors)
        else:
            self.current_display_color = self.current_color

        self.canvas.delete("all")
        text = self.current_color.upper()
        fill = self.color_values[self.current_display_color]
        if self.level == 'A':
            x0, y0 = random.randint(50, 550), random.randint(50, 350)
            self.canvas.create_oval(x0, y0, x0 + 100, y0 + 100, fill=fill, outline="")
        else:
            self.canvas.create_text(300, 200, text=text, fill=fill, font=('Helvetica', 32))

        self.event_counter += 1
        if self.event_counter < self.settings['events']:  # Schedule next stimulus only if more events are left
            interval = random.uniform(*self.settings['frequency']) * 1000
            self.root.after(int(interval), self.show_stimulus)
        else:
            print("Last event shown, finishing test.")  # Debug print
            self.root.after(0, self.finish_test)  # Ensure the test finishes after the last stimulus is shown

    def record_response(self, event):
        if not self.response_recorded:  # Check if response for the current event has been recorded
            self.response_recorded = True  # Mark the response as recorded
            selected_color = self.key_to_color.get(event.keysym.lower())
            correct = (selected_color == self.current_color if self.level != 'C' else selected_color == self.current_display_color)
            if correct:
                self.correct_answers += 1

            self.feedback_label.config(text=f"{'Correct' if correct else 'Incorrect'}. Total correct: {self.correct_answers}/{self.event_counter}")
            print(f"Response recorded. Total correct: {self.correct_answers}/{self.event_counter}")  # Debug print

    def finish_test(self):
        print("Finishing test...")  # Debug print
        total_test_time = time.time() - self.test_start_time
        correct_rate = (self.correct_answers / self.event_counter) * 100
        self.feedback_label.config(text=f"Test complete. Correct Rate: {correct_rate:.2f}%, Total Time Cost: {total_test_time:.2f} seconds")
        self.root.unbind("<KeyPress>")
        self.insert_test_data_async(self.correct_answers, correct_rate, total_test_time)

    def insert_test_data_async(self, correct_answers, correct_rate, total_time_cost):
        self.root.after(100, self.insert_test_data, correct_answers, correct_rate, total_time_cost)  # Ensure non-blocking insert
