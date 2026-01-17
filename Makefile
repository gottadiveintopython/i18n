test:
	python -m pytest ./tests

html:
	sphinx-build -b html ./sphinx ./docs
