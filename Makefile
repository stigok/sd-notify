.PHONY: build clean upload-test

build: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist *.egg-info __pycache__

upload-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
