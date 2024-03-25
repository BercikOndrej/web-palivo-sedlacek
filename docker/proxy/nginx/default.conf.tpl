server {
  gzip on;
  gzip_types      text/plain application/xml;
  gzip_proxied    no-cache no-store private expired auth;
  gzip_min_length 1000;
  gunzip on;

  listen 80;
  server_name ${DOMAIN} www.${DOMAIN};

  location /.well-known/acme-challenge/ {
    root /vol/www/;
  }

  location / {
    return 301 https://$host$request_uri;
  }
}