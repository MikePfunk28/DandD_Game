import tkinter as tk

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Security Battle - Dialogue")

        # Create the dialogue frame
        self.frame = tk.Frame(root, bg="black", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Create the dialogue text box
        self.dialogue_label = tk.Label(
            self.frame, text="", font=("Helvetica", 16), fg="white", bg="black", wraplength=400, justify="left"
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

    def add_message(self, message):
        """Add a message to the dialogue queue."""
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

class GameController:
    def __init__(self, root):
        self.ui = GameUI(root)
        self.engine = GameEngine()

        # Start the game when the UI is ready
        self.ui.add_message("Welcome to the Cloud Security Battle!")
        self.ui.add_message("Click 'Next' to start the game.")
        self.ui.next_button.config(command=self.start_game)

    def start_game(self):
        self.ui.add_message("Initializing game...")
        self.engine.initialize_game()
        self.play_next_turn()

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
