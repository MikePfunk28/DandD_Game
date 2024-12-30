from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton

from panda3d import *
# from svgutils import transform
# from panda3d import CardMaker, TransparencyAttrib, Point3, TextNode, NodePath
from direct.interval.IntervalGlobal import LerpPosInterval
from pathlib import Path
import os
import json
import random
import logging
import tempfile


# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Game Constants
GRID_SIZE = 5
ICON_SPACING = 0.5
ICON_SCALE = 0.2
PLAYER_SCALE = 0.1
ANIMATION_DURATION = 0.5
RESULT_DISPLAY_TIME = 2.0

# Colors
BACKGROUND_COLOR = (0.1, 0.1, 0.1)
TEXT_COLOR = (1, 1, 1, 1)
CORRECT_COLOR = (0, 1, 0, 1)
INCORRECT_COLOR = (1, 0, 0, 1)
BUTTON_COLOR = (0.2, 0.2, 0.2, 0.8)

# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
# Go up two levels to reach not-in-my-cloud root
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Path to icons - relative to project root
ICON_PATH = PROJECT_ROOT / "nimc" / "notinmycloud" / "src" / "aws_icons"

class CloudSecurityGame(ShowBase):
    def __init__(self):
        super().__init__()
        logger.info("Starting Cloud Security Game")

        # Set background color
        self.setBackgroundColor(*BACKGROUND_COLOR)

        # Game state
        self.board_nodes = []
        self.current_position = 0
        self.option_buttons = []
        self.score = 0

        # Load AWS icons and questions
        self.icons = self.load_aws_icons()
        self.questions_data = self.load_questions()

        # Create board and player
        self.create_board()
        self.create_player()
        self.create_score_display()

        # Setup camera
        self.setup_camera()

    def load_aws_icons(self):
        """Load AWS icons from the specified directory."""
        icons = {}
        if not ICON_PATH.exists():
            logger.error(f"Icon directory does not exist: {ICON_PATH}")
            return icons

        try:
            for icon_file in ICON_PATH.glob("*.svg"):
                try:
                    # Load SVG
                    svg_fig = transform.fromfile(str(icon_file))

                    # Create temporary PNG file
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        # Save as PNG
                        svg_fig.save(tmp_file.name)

                        # Load the PNG as texture
                        texture = self.loader.loadTexture(tmp_file.name)
                        icon_name = icon_file.stem
                        icons[icon_name] = texture
                        logger.info(f"Loaded icon: {icon_name}")

                        # Clean up temporary file
                        os.unlink(tmp_file.name)

                except ValueError as e:
                    logger.error(f"Failed to load icon {icon_file}: {e}")

        except ValueError as e:
            logger.error(f"Error in load_aws_icons: {e}")

        return icons

    def load_questions(self):
        """Load AWS icons from the specified directory."""
        icons = {}
        base_path = Path(ICON_PATH)

        if not base_path.exists():
            logger.error(f"Icon directory does not exist: {base_path}")
            return icons

        for icon_file in base_path.glob("Res_*_48.png"):
            try:
                texture = self.loader.loadTexture(str(icon_file))
                icon_name = icon_file.stem.split(
                    '_', 2)[-1]  # Extract meaningful name
                icons[icon_name] = texture
                logger.info(f"Loaded icon: {icon_name}")
            except ValueError as ve:
                logger.error(f"ValueError processing icon {
                    icon_file}: {ve}")
                logger.error(f"Failed to load icon {icon_file}: {ve}")

        return icons

    def create_board(self):
        """Create the game board with AWS icons."""
        cm = CardMaker("icon_card")
        cm.setFrame(-ICON_SCALE, ICON_SCALE, -ICON_SCALE, ICON_SCALE)

        start_x = -(GRID_SIZE * ICON_SPACING) / 2
        start_y = (GRID_SIZE * ICON_SPACING) / 2
        x, y = start_x, start_y

        for i, (icon_name, texture) in enumerate(self.icons.items()):
            # Create a card for each icon
            node = self.render2d.attachNewNode(cm.generate())
            node.setTexture(texture)
            node.setTransparency(TransparencyAttrib.MAlpha)
            node.setPos(x, 0, y)
            self.board_nodes.append(
                {"node": node, "name": icon_name, "position": (x, y)})

            # Update grid positions
            x += ICON_SPACING
            if (i + 1) % GRID_SIZE == 0:
                x = start_x
                y -= ICON_SPACING

            # Limit to GRID_SIZE * GRID_SIZE
            if len(self.board_nodes) >= GRID_SIZE * GRID_SIZE:
                break

    def create_player(self):
        """Create the player sprite."""
        cm = CardMaker("player")
        cm.setFrame(-PLAYER_SCALE, PLAYER_SCALE, -PLAYER_SCALE, PLAYER_SCALE)
        self.player = self.render2d.attachNewNode(cm.generate())
        self.player.setColor(1, 0, 0, 1)  # Red player icon

        if self.board_nodes:
            self.player.setPos(*self.board_nodes[0]["position"], 0)
        else:
            self.player.setPos(0, 0, 0)
            logger.warning("No board nodes found, placing player at center")

    def create_score_display(self):
        """Create the score display."""
        self.score_text = OnscreenText(
            text="Score: 0",
            pos=(-1.3, 0.9),
            scale=0.06,
            fg=TEXT_COLOR,
            align=TextNode.ALeft
        )

    def setup_camera(self):
        """Setup camera for 2D gameplay."""
        self.camera.setPos(0, -10, 0)
        self.camera.lookAt(Point3(0, 0, 0))

    def handle_icon_click(self, position):
        """Handle clicking an icon."""
        if self.is_valid_move(position):
            self.move_player_with_animation(position)
            self.trigger_icon_action(position)

    def is_valid_move(self, target_position):
        """Check if move is valid."""
        current_x, current_y = self.board_nodes[self.current_position]["position"]
        target_x, target_y = self.board_nodes[target_position]["position"]
        distance = abs(current_x - target_x) + abs(current_y - target_y)
        return distance <= ICON_SPACING

    def move_player_with_animation(self, target_position):
        """Move player to a new position."""
        target_x, target_y = self.board_nodes[target_position]["position"]
        LerpPosInterval(
            self.player,
            duration=ANIMATION_DURATION,
            pos=Point3(target_x, 0, target_y)
        ).start()
        self.current_position = target_position

    def trigger_icon_action(self, position):
        """Trigger action on the selected icon."""
        icon = self.board_nodes[position]
        logger.info(f"Landed on icon: {icon['name']}")
        self.show_question(icon['name'])

    def show_question(self, icon_name):
        """Display a question based on the AWS service."""
        # Clear any existing buttons
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons = []

        # Get random question
        if self.questions_data:
            question = random.choice(self.questions_data)

            # Create question text
            question_text = OnscreenText(
                text=question["question"],
                pos=(0, 0.8),
                scale=0.06,
                fg=TEXT_COLOR,
                align=TextNode.ACenter,
                wordwrap=30
            )

            # Create option buttons
            for i, option in enumerate(question["options"]):
                button = DirectButton(
                    text=option,
                    text_scale=0.04,
                    text_fg=TEXT_COLOR,
                    frameColor=BUTTON_COLOR,
                    pos=(0, 0, 0.6 - (i * 0.12)),
                    command=self.check_answer,
                    extraArgs=[option, question["answer"]]
                )
                self.option_buttons.append(button)

    def check_answer(self, selected, correct):
        """Check if the selected answer is correct."""
        if selected == correct:
            self.score += 10
            result_color = CORRECT_COLOR
            result_text = "Correct! +10 points"
        else:
            result_color = INCORRECT_COLOR
            result_text = "Incorrect"

        # Update score display
        self.score_text.setText(f"Score: {self.score}")

        # Show result
        result = OnscreenText(
            text=result_text,
            pos=(0, 0.3),
            scale=0.06,
            fg=result_color,
            align=TextNode.ACenter
        )

        # Clear result after delay
        taskMgr.doMethodLater(
            RESULT_DISPLAY_TIME, self.clear_result, 'clear_result', extraArgs=[result])

    def clear_result(self, result_text, task):
        """Clear the result text."""
        result_text.destroy()
        return task.done


if __name__ == "__main__":
    game = CloudSecurityGame()
    game.run()
