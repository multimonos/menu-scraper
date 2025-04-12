.PHONY: install watch test help

install:
	source venv/bin/activate && sleep 3 && pip install playwright && playwright install chromium && pip install -r requirements.txt

test:
	pytest -s ./src/*.py

watch:
	ls ./src/*.py |entr -c pytest -s ./src/*.py

help:
	python src/main.py --help


