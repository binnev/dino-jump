install:
	python3 -m venv ./venv
	. ./venv/bin/activate
	pip install -r requirements.txt

play:
	python3 game.py