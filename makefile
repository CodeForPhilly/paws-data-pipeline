# Make File to simplify running various docker-compose setups
# for testing

CC = sudo docker-compose
secrets_dict = ./src/server/secrets_dict.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
	   	| sort \
	   	| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


dependency: $(secrets_dict)

build: dependency  ## Clean build of the Server App
	@cd src &&\
		$(CC) build

run: build## Run the full application ( docker-compose up )
	@cd src &&\
		$(CC) up --detach

docker-server: build
	@cd src &&\
	    $(CC) run --detach server

local-client: docker-server ## Run front-end locally, back-end in Docker
	@cd src/client && yarn run start:local&

local-server:  ## Run back-end locally, Database in Docker
	@cd src &&\
	    export PAWS_API_HOST=localhost &&\
	    $(CC) up --detach &&\
		$(CC) stop server &&\
		export IS_LOCAL=True &&\
		cd server &&\
		flask run
		

all: clean build run ## Clean, Build, then Run

clean: ## Remove containers and networks (docker-compose down)
	@cd src &&\
	    $(CC) down
