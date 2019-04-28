PIPENV=.venv
PYTHON_VERSION=3.7

.PHONY: all test

all: $(PIPENV)

$(PIPENV):
	env PIPENV_VENV_IN_PROJECT=$(PIPENV) pipenv --python $(PYTHON_VERSION)
	pipenv install

test: $(PIPENV)
	pipenv install -d
	pipenv run pylint vault.py
	env PYTHONPATH=. pipenv run pytest -v --doctest-modules --color=yes tests/


.PHONY: clean-env


clean-env:
	rm -rf $(PIPENV) Pipfile.lock
