# Makefile
# Auto-detects whether to use 'docker-compose' or 'docker compose'
COMPOSE
_
CMD := $(shell command -v docker-compose 2>/dev/null)
ifeq ($(COMPOSE
_
CMD),)
COMPOSE
_
CMD := docker compose
endif
.PHONY: all up down clean logs
# Default command
all: up
# Build and start the application
up:
@echo "Starting application...
@$(COMPOSE
_
CMD) up --build -d
"
# Stop the application
down:
@echo "Stopping application...
@$(COMPOSE
CMD) down
_
"
# Clean up the environment
clean: down
@echo "Cleaning up generated files...
@rm -rf ./models ./data ./__pycache
__
"
# View application logs
logs:
@echo "Tailing logs...
"
@$(COMPOSE
_
CMD) logs -f