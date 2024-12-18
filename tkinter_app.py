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
