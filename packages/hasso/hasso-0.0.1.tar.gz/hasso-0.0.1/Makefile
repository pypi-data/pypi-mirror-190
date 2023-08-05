init:
	@python3 -m venv env
	@echo "env" >> .gitignore
	. env/bin/activate

dep:
	@pip freeze > requirement.txt

all:
	./env/bin/python work.py


build:
	python -m pip install --upgrade build
	python -m build


.PHONY:
	init dep all build
