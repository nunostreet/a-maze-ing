.PHONY: install run debug clean lint lint-strict

PYTHON := python3
MAIN := a_maze_ing.py
CONFIG ?= config.txt

install:
	PYENV_DISABLE_AUTO_REHASH=1 $(PYTHON) -m pip install --upgrade pip
	PYENV_DISABLE_AUTO_REHASH=1 $(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	$(PYTHON) -m flake8 . --exclude .venv
	$(PYTHON) -m mypy . --exclude '.venv/' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --exclude .venv
	$(PYTHON) -m mypy . --exclude '.venv/' --strict
