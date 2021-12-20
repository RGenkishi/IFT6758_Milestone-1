#!/bin/bash

cp ./requirements.txt ./docker-project-template/requirements.txt
cd ./docker-project-template
docker build -t serving -f Dockerfile.serving .