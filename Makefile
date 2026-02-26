.PHONY: install run debug clean lint lint-strict package

# Prefer the local virtualenv Python when available.
PYTHON := $(if $(wildcard .venv/bin/python3),.venv/bin/python3,python3)
MAIN := a_maze_ing.py
CONFIG ?= config.txt
# Keep a single distributable at repository root for evaluation.
PACKAGE_KIND ?= whl
# Restrict linting to project code only.
LINT_TARGETS := maze io_helpers render a_maze_ing.py

# Install/update project tooling in the active Python.
install:
	PYENV_DISABLE_AUTO_REHASH=1 $(PYTHON) -m pip install --upgrade pip
	PYENV_DISABLE_AUTO_REHASH=1 $(PYTHON) -m pip install setuptools wheel build
	PYENV_DISABLE_AUTO_REHASH=1 $(PYTHON) -m pip install -r requirements.txt

# Run application with optional CONFIG override.
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# Start interactive debugger for the app entrypoint.
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Remove caches and packaging artifacts.
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist build
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +

# Standard lint/type checks.
lint:
	$(PYTHON) -m flake8 $(LINT_TARGETS)
	$(PYTHON) -m mypy $(LINT_TARGETS) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Strict type checking profile.
lint-strict:
	$(PYTHON) -m flake8 $(LINT_TARGETS)
	$(PYTHON) -m mypy $(LINT_TARGETS) --strict

# Build package artifacts and copy one selected file to repository root.
package:
	$(PYTHON) -m pip show build >/dev/null 2>&1 || (echo "Run 'make install' first (build missing)." && exit 1)
	$(PYTHON) -m build --no-isolation
	@if [ "$(PACKAGE_KIND)" = "tar" ]; then \
		cp -f dist/*.tar.gz .; \
		rm -f ./*.whl; \
		echo "Kept tar.gz at repository root."; \
	else \
		cp -f dist/*.whl .; \
		rm -f ./*.tar.gz; \
		echo "Kept wheel at repository root."; \
	fi
