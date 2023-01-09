install:
	python -m pip install -r requirements.txt
	python -m pip install isort black

clean:
	python -m isort */*.py
	python -m black */*.py
