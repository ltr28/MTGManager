install:
	pip install --upgrade pip &&\
	pip install -e .

lint:
	ruff check .

test:
	python -m pytest .
