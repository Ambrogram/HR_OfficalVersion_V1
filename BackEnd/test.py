import tkinter as tk
import random
import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a reaction time test.")
    parser.add_argument("--eventsCount", type=int, default=102, help="Number of events in the test")
    parser.add_argument("--frequencyRange", type=int, default=1000, help="Frequency range in milliseconds between events")
    return parser.parse_args()

def main():
    global event_counter, correct_answers, current_color, test_start_time
    args = parse_arguments()
    
    
    # Initialize variables
    event_counter = 0
    correct_answers = 0
    current_color = ''
    current_display_color = ''
    level = ''
    test_start_time = time.time()
    
    
    # Setup the main window
    root = tk.Tk()
    root.title("Reaction Time Test")
    

    # Settings based on arguments
    frequency_range = args.frequencyRange
    total_events = args.eventsCount

    
    # Colors setup
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan']
    color_values = {
        'red': '#FF0000',
        'blue': '#0000FF',
        'green': '#008000',
        'yellow': '#FFFF00',
        'purple': '#800080',
        'orange': '#FFA500',
        'cyan': '#00FFFF'
    }
    key_to_color = {
        'r': 'red',
        'b': 'blue',
        'g': 'green',
        'y': 'yellow',
        'p': 'purple',
        'o': 'orange',
        'c': 'cyan'
    }
    
    
    canvas = tk.Canvas(root, width=600, height=400, bg='white')
    canvas.pack()

    feedback_label = tk.Label(root, text="", font=('Helvetica', 16))
    feedback_label.pack(pady=10)
    
    def show_stimulus():
        global current_color, current_display_color, level, event_counter
        if event_counter < args.eventsCount:
            level = random.choice(['A', 'B', 'C'])
            current_color = random.choice(colors)
            if level == "C":
                mismatch_colors = [c for c in colors if c != current_color]
                current_display_color = random.choice(mismatch_colors)
            else:
                current_display_color = current_color

            canvas.delete("all")
            text = current_color.upper()
            fill = color_values[current_display_color]
            if level == 'A':
                x0, y0 = random.randint(50, 550), random.randint(50, 350)
                canvas.create_oval(x0, y0, x0 + 100, y0 + 100, fill=fill, outline="")
            else:
                canvas.create_text(300, 200, text=text, fill=fill, font=('Helvetica', 32))
            event_counter += 1
            root.after(args.frequencyRange, show_stimulus)
    
    
        
    def record_response(event):
        global event_counter, correct_answers, current_color, current_display_color, level, test_start_time
        selected_color = key_to_color.get(event.keysym.lower())
        correct = (selected_color == current_color if level != 'C' else selected_color == current_display_color)
        if correct:
            correct_answers += 1
            
        # Update feedback label with the current number of correct answers    
        feedback_label.config(text=f"{'Correct' if correct else 'Incorrect'}. Total correct: {correct_answers}/{event_counter}")
        if event_counter >= args.eventsCount:
            
            # Calculate total test time when the test is complete
            total_test_time = time.time() - test_start_time
            
            # Calculate the correct rate as a percentage
            correct_rate = (correct_answers / event_counter) * 100
            
            # Update feedback label to show the correct rate and total test time
            feedback_label.config(text=f"Test complete. Correct Rate: {correct_rate:.2f}%, Total Time Cost: {total_test_time:.2f} seconds")
            
            # Unbind keypress event to stop taking input after the test ends
            root.unbind("<KeyPress>")



        
    root.bind("<KeyPress>", record_response)
    show_stimulus()
    root.mainloop()

if __name__ == "__main__":
    main()
