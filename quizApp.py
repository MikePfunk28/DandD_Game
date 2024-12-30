from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence  # Add this import
from panda3d.core import TextNode, Point3, PointLight
import json
import os
import math


class Quiz3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load questions
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, 'questions.json')

        with open(json_path, 'r') as file:
            self.questions = json.load(file)

        self.current_question = 0
        self.score = 0

        # Create a background frame
        self.bg_frame = DirectFrame(
            frameColor=(0.2, 0.2, 0.2, 0.8),
            frameSize=(-1, 1, -1, 1),
            pos=(0, 0, 0)
        )

        # Create question frame
        self.question_frame = DirectFrame(
            frameColor=(0.3, 0.3, 0.3, 0.9),
            frameSize=(-1, 1, -0.2, 0.2),
            pos=(0, 0, 0.7)
        )

        # Create question text
        self.question_text = OnscreenText(
            text="",
            pos=(0, 0.7),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            wordwrap=30,
            parent=self.question_frame
        )

        # Create options frame
        self.options_frame = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.9, 0.9, -0.5, 0.5),
            pos=(0, 0, 0)  # Centered position
        )

        # Create option buttons
        self.option_buttons = []
        self.create_buttons()

        # Setup camera and lighting
        self.setup_camera()
        self.setup_lighting()

        # Display first question
        self.display_question()

    def create_buttons(self):
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons = []

        # Button properties
        button_props = {
            'frameSize': (-0.8, 0.8, -0.08, 0.08),
            'text_scale': 0.06,
            'text_align': TextNode.ALeft,
            'text_pos': (-0.7, -0.02),
            'relief': DirectButton.RAISED,
            'borderWidth': (0.005, 0.005)
        }

        # Colors for different button states
        button_colors = (
            (0.3, 0.3, 0.3, 1),  # Normal
            (0.4, 0.4, 0.4, 1),  # Click
            (0.5, 0.5, 0.5, 1),  # Hover
            (0.2, 0.2, 0.2, 1)   # Disabled
        )

        # Centered vertical positions
        y_positions = [0.3, 0.1, -0.1, -0.3]
        for i in range(4):
            button = DirectButton(
                parent=self.options_frame,
                pos=(0, 0, y_positions[i]),  # Centered horizontally
                command=self.check_answer,
                extraArgs=[i],
                frameColor=button_colors,
                rolloverSound=None,  # Disable default sound
                clickSound=None,     # Disable default sound
                **button_props
            )
            # Add hover and click events
            button.bind(DirectButton.ENTER, lambda x,
                        b=button: self.animate_button_hover(b))
            button.bind(DirectButton.EXIT, lambda x,
                        b=button: self.animate_button_hover(b, reverse=True))
            button.bind(DirectButton.B1PRESS, lambda x,
                        b=button: self.animate_button_click(b))

            self.option_buttons.append(button)

    def animate_button_hover(self, button, reverse=False):
        scale = 0.95 if reverse else 1.05
        button.scaleInterval(0.1, scale).start()

    def animate_button_click(self, button):
        sequence = Sequence(
            button.scaleInterval(0.1, 0.9),
            button.scaleInterval(0.1, 1.0)
        )
        sequence.start()

    def transition_to_next_question(self):
        # Slide current question out
        current_pos = self.question_frame.getPos()
        self.question_frame.posInterval(
            0.5, Point3(2, 0, current_pos.z)).start()

        # Slide new question in
        self.question_frame.setPos(-2, 0, current_pos.z)
        self.question_frame.posInterval(0.5, current_pos).start()

    def display_question(self):
        if self.current_question >= len(self.questions):
            self.show_final_score()
            return

        question = self.questions[self.current_question]
        self.question_text.setText(question["question"])

        for i, (letter, text) in enumerate(question["options"].items()):
            self.option_buttons[i]['text'] = f"{letter}. {text}"

        # Add transition effect
        self.transition_to_next_question()

    # ... (rest of the methods remain the same)


if __name__ == "__main__":
    app = Quiz3D()
    app.run()
