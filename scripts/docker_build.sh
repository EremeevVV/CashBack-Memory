#!/bin/bash
set -o allexport && source .env && set +o allexport
last_version=$(scripts/get_last_version.sh)
new_version=$(($last_version+1))

USER_ID=$(id -u $USERNAME) GROUP_ID=$(id -g $USERNAME)  VERSION=$new_version docker-compose -f docker-compose.yaml build
