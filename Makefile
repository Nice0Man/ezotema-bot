.PHONY: build up down logs

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

rebuild:
	docker-compose up -d --build

stop:
	docker-compose stop

start:
	docker-compose start