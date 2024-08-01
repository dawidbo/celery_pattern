#!/bin/bash

# Zatrzymanie kontenerów
docker stop flask_app celery_worker celery_beat redis

# Usunięcie kontenerów
docker rm flask_app celery_worker celery_beat redis
