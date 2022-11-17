filename ?=

init:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up -d

server:
	docker-compose -f docker-compose.yml exec eshiritori-api python3 manage.py runserver 0.0.0.0:8000

migrate:
	docker-compose -f docker-compose.yml exec eshiritori-api python3 manage.py makemigrations
	docker-compose -f docker-compose.yml exec eshiritori-api python3 manage.py migrate

down:
	docker-compose -f docker-compose.yml down

install:
	docker-compose -f docker-compose.yml exec eshiritori-api pip install -r requirements.txt

create-super-user:
	docker-compose -f docker-compose.yml exec eshiritori-api python3 manage.py createsuperuser

run:
	docker-compose -f docker-compose.yml exec eshiritori-api python3 ${filename}