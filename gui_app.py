from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import CardMaker, TransparencyAttrib, Point3
from direct.interval.IntervalGlobal import LerpPosInterval
from pathlib import Path
import json
import random
import logging

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

# Colors
BACKGROUND_COLOR = (0.1, 0.1, 0.1)
TEXT_COLOR = (1, 1, 1, 1)

# Icon Path
ICON_PATH = "C:/Users/mikep/not-in-my-cloud/nimc/notinmycloud/src/aws_icons/Resource-Icons_06072024"


class CloudSecurityGame(ShowBase):
    def __init__(self):
        super().__init__()
        logger.info("Starting Cloud Security Game")

        # Set background color
        self.setBackgroundColor(*BACKGROUND_COLOR)

        # Game state
        self.board_nodes = []
        self.current_position = 0

        # Load AWS icons
        self.icons = self.load_aws_icons()

        # Create board and player
        self.create_board()
        self.create_player()

        # Setup camera
        self.setup_camera()

    def load_aws_icons(self):
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
            except Exception as e:
                logger.error(f"Failed to load icon {icon_file}: {e}")

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
        self.player.setColor(1, 0, 0, 1)  # Red color for player sprite
        self.player.setPos(*self.board_nodes[0]["position"], 0)

    def setup_camera(self):
        """Setup camera for 2D gameplay."""
        self.camera.setPos(0, -10, 0)
        self.camera.lookAt(0, 0, 0)

    def handle_icon_click(self, position):
        """Handle clicking an icon."""
        if self.is_valid_move(position):
            self.move_player_with_animation(position)
            logger.info(f"Landed on icon: {
                        self.board_nodes[position]['name']}")

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
            pos=(target_x, 0, target_y)
        ).start()
        self.current_position = target_position


if __name__ == "__main__":
    game = CloudSecurityGame()
    game.run()
