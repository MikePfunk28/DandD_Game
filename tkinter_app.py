import tkinter as tk
from game_engine import GameEngine

class GameUI:
    def __init__(self, root, font_style=("Helvetica", 16), text_color="white", bg_color="black", max_messages=100):
        self.root = root
        self.root.title("Cloud Security Battle - Dialogue")

        # Create the dialogue frame
        self.frame = tk.Frame(root, bg=bg_color, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Create the dialogue text box
        self.dialogue_label = tk.Label(
            self.frame, text="", font=font_style, fg=text_color, bg=bg_color, wraplength=400, justify="left"
        )
        self.dialogue_label.pack(pady=20)

        # Create the "Next" button
        self.next_button = tk.Button(
            self.frame, text="Next", command=self.next_message, font=("Helvetica", 12), bg="blue", fg="white"
        )
        self.next_button.pack()

        # Dialogue message queue
        self.messages = []
        self.current_message_index = 0
        self.max_messages = max_messages

    def add_message(self, message):
        """Add a message to the dialogue queue."""
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)  # Remove the oldest message to maintain the queue size
        self.messages.append(message)
        if len(self.messages) == 1:  # If this is the first message, display it immediately
            self.show_message()

    def show_message(self):
        """Display the current message."""
        if self.current_message_index < len(self.messages):
            self.dialogue_label.config(text=self.messages[self.current_message_index])
        else:
            self.dialogue_label.config(text="End of dialogue.")

    def next_message(self):
        """Move to the next message in the queue."""
        self.current_message_index += 1
        if self.current_message_index < len(self.messages):
            self.show_message()
        else:
            self.dialogue_label.config(text="End of dialogue.")
            self.next_button.config(state="disabled")

    def reset_ui(self):
        """Resets the UI components to prepare for a new game."""
        self.messages.clear()
        self.current_message_index = 0
        self.dialogue_label.config(text="")
        self.next_button.config(state="normal")

    def show_options(self, prompt, options, callback):
        """Display a set of options to the user and handle their selection."""
        self.add_message(prompt)

        def on_option_selected(option):
            callback(option)
            for button in option_buttons:
                button.destroy()

        option_buttons = []
        for option in options:
            button = tk.Button(
                self.frame, text=option, font=("Helvetica", 12), bg="lightblue", command=lambda opt=option: on_option_selected(opt)
            )
            button.pack(pady=5)
            option_buttons.append(button)

class GameController:
    def __init__(self, root):
        self.ui = GameUI(root)
        self.engine = GameEngine()

        # Start the game when the UI is ready
        self.ui.add_message("Welcome to the Cloud Security Battle!")
        self.ui.add_message("Click 'Next' to start the game.")
        self.ui.next_button.config(command=self.start_game)

    def start_game(self):
        self.ui.reset_ui()  # Reset UI to handle clean restarts
        self.ui.add_message("Initializing game...")
        self.ui.add_message("Enter the number of players:")

        def on_players_entered():
            try:
                number_of_players = int(entry.get())
                entry.delete(0, tk.END)  # Clear the entry field
                entry.config(state="disabled")  # Disable the entry field
                submit_button.config(state="disabled")  # Disable the submit button
                self.engine.initialize_game(number_of_players)
                self.play_next_turn()
            except ValueError:
                self.ui.add_message("Invalid input. Please enter a number.")

        entry = tk.Entry(self.ui.frame, font=("Helvetica", 12))
        entry.pack()
        submit_button = tk.Button(
            self.ui.frame, text="Submit", command=on_players_entered, font=("Helvetica", 12), bg="green", fg="white"
        )
        submit_button.pack()

    def play_next_turn(self):
        self.ui.add_message("Playing the next turn...")
        # Logic to play a turn via the GameUI (replace print and input)

        # Example of using the GameUI for input:
        def on_user_choice(choice):
            self.ui.add_message(f"You selected: {choice}")
            # Handle game logic based on choice

        self.ui.show_options(
            "What would you like to do?",
            ["Roll dice", "Draw card"],
            callback=on_user_choice
        )

if __name__ == "__main__":
    root = tk.Tk()
    controller = GameController(root)
    root.mainloop()
