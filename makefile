install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C ManageMTG/datasets/

test:
	python -m pytest .