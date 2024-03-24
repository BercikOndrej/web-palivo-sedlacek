#!/bin/sh

set -e

# Path to folder where is located docker-compose.yml file
cd <path_to_project_folder>
docker-compose run --rm certbot certbot renew