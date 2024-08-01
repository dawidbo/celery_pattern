#!/bin/bash

# Budowanie obrazów
docker build -t flask_app -f Dockerfile .
docker build -t celery_worker -f Dockerfile.celery .
docker build -t celery_beat -f Dockerfile.celery_beat .

# Uruchomienie kontenerów
docker run -d --name redis --network my_network -p 6379:6379 redis:latest
docker run -d --name flask_app --network my_network -p 5000:5000 flask_app
docker run -d --name celery_worker --network my_network celery_worker 
docker run -d --name celery_beat --network my_network celery_beat
