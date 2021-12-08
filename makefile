# Make File to simplify running various docker-compose setups
# for testing


secrets_dict = ./src/server/secrets_dict.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
	   	| sort \
	   	| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


deps: $(secrets_dict)

build: deps  ## Clean build of the Server App
	@cd src && sudo docker-compose build

run: ## Run the full application ( docker-compose up )
	@cd src && sudo docker-compose up

docker-server:
	@cd src && sudo docker-compose run server

local-client: docker-server ## Run front-end locally, back-end in Docker
	@cd src && npm run start:local

local-server:  ## Run back-end locally, Database in Docker
	@cd src &&\
	   	export PAWS_API_HOST=localhost &&\
	   	sudo docker-compose up &&\
		sudo docker stop paws-compose-server

all: clean build run ## Clean, Build, then Run

clean: ## Remove containers and networks (docker-compose down)
	@cd src && sudo docker-compose down
