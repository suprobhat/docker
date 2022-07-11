#! /bin/bash
sed -n '/image:/p' docker-compose.yaml
sed -i '/image:/c\    image: gcr.io/subhamrd-353905/back-end:v1.1.${IMAGE_VERSION}' docker-compose.yaml
