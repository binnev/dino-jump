import glob
import os
import subprocess
import sys
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
    # record_last_n_frames = 60 * 60 * 2
    # recording_dir = Path(__file__).parent / "recordings"

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
        try:
            super().main()
        except SystemExit:
            if self.record_last_n_frames:
                self.clean_empty_recordings_dir()
                self.save_screenshots()
                self.create_videos()
        pygame.quit()
        sys.exit()

    def clean_empty_recordings_dir(self):
        try:
            os.mkdir(self.recording_dir.as_posix())
        except FileExistsError:
            pass

        # clear old files
        files = glob.glob((self.recording_dir / "*").as_posix())
        for file in files:
            os.remove(file)

    def save_screenshots(self):
        for ii, image in enumerate(self.screenshots):
            pygame.image.save(image, str(self.recording_dir / f"{ii}.png"))

    def create_videos(self):
        subprocess.run(
            [
                "ffmpeg",
                "-r",
                "60",
                "-i",
                str(self.recording_dir / "%d.png"),
                "-r",
                "60",
                str(self.recording_dir / "out.mp4"),
            ]
        )
        subprocess.run(
            [
                "ffmpeg",
                "-r",
                "60",
                "-i",
                str(self.recording_dir / "%d.png"),
                "-filter_complex",
                # credit: https://superuser.com/questions/1049606/reduce-generated-gif-size-using-ffmpeg
                (
                    "fps=30,"
                    "scale=1080:-1:flags=lanczos,"
                    "split[s0][s1];[s0]"
                    "palettegen=max_colors=32[p];[s1][p]"
                    "paletteuse=dither=bayer"
                ),
                str(self.recording_dir / "out.gif"),
            ]
        )


if __name__ == "__main__":
    DinoJump().main()
