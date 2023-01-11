all: format lint

lint:
	flake8 gsrest

format:
	autopep8 --in-place --recursive gsrest
	yapf --in-place --recursive gsrest
	

.PHONY: format lint
