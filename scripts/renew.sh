#!/bin/sh

set -e

cd /home/<user>/<project_name>
/usr/local/bin/docker-compose --rm certbot certbot renew