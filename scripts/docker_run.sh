#!/bin/bash
set -o allexport && source .env && set +o allexport
last_version=$(scripts/get_last_version.sh)

docker stop cashback_memory
USER_ID=$(id -u $USERNAME) GROUP_ID=$(id -g $USERNAME) VERSION=$last_version docker-compose -f docker-compose.yaml up -d
