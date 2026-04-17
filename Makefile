PYTHON = .venv/bin/python
PIP = .venv/bin/pip

MAIN = a_maze_ing.py
CONFIG = config.txt

install:
	test -d .venv || python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install build

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f maze.txt
	rm -f backup.txt

fclean:clean
	rm -r .venv
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

re: clean run

lint:
	$(PYTHON) -m flake8 . --exclude .venv
	$(PYTHON) -m mypy . \
		--exclude .venv \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --exclude .venv
	$(PYTHON) -m mypy . --strict --exclude .venv

test:
	$(PYTHON) -m pytest

build:
	$(PYTHON) -m build

.PHONY: install run debug clean fclean re lint lint-strict test build