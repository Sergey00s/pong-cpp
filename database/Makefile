
VOLUME = postgres_data
SERVICE = postgres
COMPOSE_FILE = docker-compose.yml
PS = docker compose -f $(COMPOSE_FILE) ps

IMAGES = $(shell docker images -q)

up: 
	mkdir -p /var/volumes/$(VOLUME)
	docker compose -f $(COMPOSE_FILE) up -d


down:
	docker compose -f $(COMPOSE_FILE) down


clean:
	docker compose -f $(COMPOSE_FILE) down -v
	docker volume rm $(VOLUME)
	docker rm $(SERVICE)

fclean: clean
	docker rmi $(IMAGES)
	
re: fclean up