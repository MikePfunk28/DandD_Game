import json
import tkinter as tk
from tkinter import ttk, messagebox
import os


class QuizApp:
    def __init__(self, window):
        self.window = window
        self.window.title("AWS Architecture Quiz")
        self.window.geometry("800x600")

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the full path to questions.json
        json_path = os.path.join(script_dir, 'questions.json')

        # Load questions using absolute path
        try:
            with open(json_path, 'r') as file:
                self.questions = json.load(file)
        except FileNotFoundError:
            messagebox.showerror(
                "Error", f"Could not find questions.json at:\n{json_path}")
            self.window.quit()
            return
        except json.JSONDecodeError:
            messagebox.showerror(
                "Error", "questions.json is not properly formatted")
            self.window.quit()
            return

        self.score = 0
        self.current_question = 0

        # Create main frame
        self.main_frame = ttk.Frame(window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Question label
        self.question_label = ttk.Label(
            self.main_frame,
            wraplength=700,
            justify="left"
        )
        self.question_label.grid(row=0, column=0, pady=20)

        # Options frame
        self.options_frame = ttk.Frame(self.main_frame)
        self.options_frame.grid(row=1, column=0, pady=10)

        # Radio buttons for options
        self.selected_option = tk.StringVar()
        self.option_buttons = {}

        # Score label
        self.score_label = ttk.Label(
            self.main_frame,
            text=f"Score: {self.score}/{len(self.questions)}"
        )
        self.score_label.grid(row=3, column=0, pady=10)

        # Submit button
        self.submit_btn = ttk.Button(
            self.main_frame,
            text="Submit",
            command=self.check_answer
        )
        self.submit_btn.grid(row=2, column=0, pady=20)

        # Display first question
        self.display_question()

    def display_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=question["question"])

        # Clear existing options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Create new option buttons
        for i, (letter, text) in enumerate(question["options"].items()):
            # Create a frame for each option
            option_frame = ttk.Frame(self.options_frame)
            option_frame.grid(row=i, column=0, sticky="w", pady=2)

            # Radio button (without text)
            rb = ttk.Radiobutton(
                option_frame,
                value=letter,
                variable=self.selected_option,
                padding=5
            )
            rb.grid(row=0, column=0, sticky="w")

            # Label for option text
            label = ttk.Label(
                option_frame,
                text=f"{letter}. {text}",
                wraplength=600,
                justify="left"
            )
            label.grid(row=0, column=1, sticky="w", padx=5)

            self.option_buttons[letter] = rb

    def check_answer(self):
        if not self.selected_option.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        question = self.questions[self.current_question]
        if self.selected_option.get() == question["answer"]:
            self.score += 1
            messagebox.showinfo("Correct!", question["explanation"])
        else:
            correct_answer = question["answer"]
            correct_text = question["options"][correct_answer]
            messagebox.showinfo("Incorrect",
                                f"The correct answer was {correct_answer}: {correct_text}\n\n{question['explanation']}")

        self.score_label.config(
            text=f"Score: {self.score}/{len(self.questions)}")
        self.next_question()

    def next_question(self):
        self.current_question += 1
        self.selected_option.set("")  # Clear selection

        if self.current_question < len(self.questions):
            self.display_question()
        else:
            final_score = (self.score / len(self.questions)) * 100
            messagebox.showinfo("Quiz Complete",
                                f"Quiz finished!\nFinal Score: {final_score:.2f}%")
            self.window.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
