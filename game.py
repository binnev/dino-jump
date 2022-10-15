import glob
import os
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import pygame
from pygame.surface import Surface

from robingame.objects import Game
import conf
from scenes import DinoJumpManager


class DinoJump(Game):
    window_width = conf.WINDOW_WIDTH
    window_height = conf.WINDOW_HEIGHT
    window_caption = "Dino Jump"
    screen_color = (130, 130, 130)
    record_last_n_frames = 60  # * 60 * 5

    def __init__(self):
        super().__init__()
        pygame.mouse.set_visible(0)
        self.scenes.add(DinoJumpManager())
        if self.record_last_n_frames:
            self.screenshots = deque(maxlen=self.record_last_n_frames)

    def _draw(self, surface: Surface, debug: bool = False):
        super()._draw(surface, debug)
        if self.record_last_n_frames:
            screenshot = Surface(surface.get_size()).convert_alpha()
            super()._draw(screenshot, debug)
            self.screenshots.append(screenshot)

    def main(self):
        """This is the outermost game function which runs once. It contains the outermost game
        loop. Here's where you should put your main event state machine."""
        self.running = True

        try:
            while self.running:
                self._update()
                self._draw(self.window, debug=self.debug)
        except SystemExit:
            if self.record_last_n_frames:
                # make sure recordings dir exists
                folder = Path(__file__).parent / "recordings"
                try:
                    os.mkdir(folder.as_posix())
                except FileExistsError:
                    pass

                # clear old files
                files = glob.glob((folder / "*.*").as_posix())
                for file in files:
                    os.remove(file)

                # export in-memory screenshots
                for ii, image in enumerate(self.screenshots):
                    filename = Path(__file__).parent / f"recordings/{ii}.png"
                    pygame.image.save(image, filename.as_posix())

                # stitch them together
                subprocess.run(
                    [
                        "ffmpeg",
                        "-r",
                        "60",
                        "-i",
                        str(folder / "%d.png"),
                        "-r",
                        "30",
                        str(folder / "out.gif"),
                    ]
                )
                subprocess.run(
                    [
                        "ffmpeg",
                        "-r",
                        "60",
                        "-i",
                        str(folder / "%d.png"),
                        "-r",
                        "60",
                        str(folder / "out.mp4"),
                    ]
                )

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    DinoJump().main()
