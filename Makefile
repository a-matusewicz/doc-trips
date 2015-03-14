
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
COVERAGE=$(VENV)/bin/coverage
MANAGE=$(PYTHON) manage.py

.PHONY: install migrations migrate test coverage clean deploy

all:
	$(MANAGE) runserver

install:
	pyvenv $(VENV)
	$(PIP) install -r requirements.txt

deploy: 
	heroku maintenance:on
	git push heroku master
	heroku run migrate
	heroku maintenance:off

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) setsuperuser d34898x

test: 
	$(MANAGE) test --nomigrations

coverage:
	$(COVERAGE) run --omit "$(VENV)/*" manage.py test --nomigrations
	$(COVERAGE) report -m
	$(COVERAGE) html 

clean: 
	rm -rf *.pyc
	rm -rf *~
