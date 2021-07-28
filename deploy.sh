#!/bin/sh
sudo git config core.sshCommand 'ssh -i "{$PRIVATE_KEY_GITHUB_ACTIONS}"' && \
cd Django-Movie-Database/ && \
sudo git pull && \
sudo docker-compose up -d --build