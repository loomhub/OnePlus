install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt	
format:
	#format
	black *.py controllers/*.py dtos/*.py models/*.py repositories/*.py services/*.py
lint:
	#pylint
	pylint --disable=R,C *.py controllers/*.py dtos/*.py models/*.py repositories/*.py services/*.py
test:
	#test
	#python -m pytest -vv --cov=mylib --cov=main test_*.py
build:
	#build container
	#docker build -t deploy-fastapi .
run:
	#run docker build
	#docker run -p 127.0.0.1:8080:8080 734519d16822
deploy:
	#deploy
all: install format lint test deploy