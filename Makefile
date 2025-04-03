.PHONY: install \
	scrape \
	watch \
	test \
	parse-all \
	parse-food \
	parse-drink \
	parse-happy


install:
	source venv/bin/activate && pip install playwright && playwright install chromium && pip install -r requirements.txt

test:
	pytest -s ./src/*.py

watch:
	ls ./src/*.py |entr -c pytest -s ./src/*.py

help:
	python src/main.py --help

scrape:
	# ls src/*.py | entr -c bash -c "clear && python -u src/main.py scrape https://cactus.test"
	rm -rf ./data/*.html  \
  && python -u src/main.py scrape https://cactus.test


parse-all:
	parse-all.sh

parse-drink:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--drink.html

parse-food:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--food.html

parse-happy:
	ls src/*.py | entr python -u src/main.py parse data/cactus-test-locations-crowfoot-menu--happy-hour.html

