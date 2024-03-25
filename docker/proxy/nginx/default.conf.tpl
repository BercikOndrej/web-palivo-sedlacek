server {
  gzip              on;
  gzip_disable      "MSIE [1-6]\.(?!.*SV1)";
  gzip_vary         on;
  gzip_types        text/plain application/xml text/css text/javascript image/svg+xml image/x-icon application/javascript application/x-javascript;
  gunzip            on;

  listen 80;
  server_name ${DOMAIN} www.${DOMAIN};

  location /.well-known/acme-challenge/ {
    root /vol/www/;
  }

  location / {
    return 301 https://$host$request_uri;
  }
}