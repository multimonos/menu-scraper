.PHONY: install \
	scrape \
	watch \
	test \
	parse-food \
	parse-drink \
	parse-happy \
	parse-food-csv \
	parse-drink-csv \
	parse-happ-csv

install:
	source venv/bin/activate && sleep 3 && pip install playwright && playwright install chromium && pip install -r requirements.txt

test:
	pytest -s ./src/*.py

watch:
	ls ./src/*.py |entr -c pytest -s ./src/*.py

help:
	python src/main.py --help

scrape:
	rm -rf ./data/*.html  \
  && python -u src/main.py scrape https://cactus.test

parse-drink-csv:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--drink.html --output=data/cactus-test-locations-crowfoot-menu--drink.csv
parse-food-csv:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--food.html --output=data/cactus-test-locations-crowfoot-menu--food.csv
parse-happy-hour-csv:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--happy-hour.html --output=data/cactus-test-locations-crowfoot-menu--happy-hour.csv

parse-drink:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--drink.html
parse-food:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--food.html
parse-happy:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--happy-hour.html

