install:
	pip install --upgrade pip &&\
	pip install -e .

lint:
	pylint --disable=R,C ManageMTG/datasets/

test:
	python -m pytest .