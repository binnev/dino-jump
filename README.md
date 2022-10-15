# Dino Jump

The long-awaited sequel to the [Chrome dinosaur game](chrome://dino/). Built entirely in [pygame](https://pypi.org/project/pygame/) and [robingame](https://pypi.org/project/robingame/).

## This time Dino came strapped.

Press `G` to shoot the gun and give those cacti a fatal dose of lead. Watch out though: shooting cacti lowers your
score.

![Shooting angles](readme_media/shooting.gif)

Use the arrow keys to angle your gun:

![Shooting angles](readme_media/shooting_angles.gif)

You can use this to shoot Dino's mortal enemy: Pterodactyl. Popping a pterodactyl nets you 100 points.

![Shooting angles](readme_media/pterodactyl.gif)

Those are the controls. If you forgot any of that, just hit escape to see this sweet pause menu, complete with dino claw
cursor that does ___absolutely nothing___.

![Shooting angles](readme_media/pausemenu.gif)

Sometimes even a rain of hot lead can't stop the cacti. If Dino bites the dust, be sure to enter his/her name in the
highscores.

![Shooting angles](readme_media/highscore.gif)

Just don't put a space in the name; that'll start a new game. It's a bug. I'm working on it. Give me a break, I built
all this from scratch including the text input field. 


## Installation
Dino Jump requires python >= 3.10 and pip, so make sure you have those installed. See [the Python downloads page](https://www.python.org/downloads/) for help on that.
```
pip install -r requirements.txt
```

Then, navigate to the project directory and run 
```
python game.py
```