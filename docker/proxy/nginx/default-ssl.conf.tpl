server {
  gzip              on;
  gzip_disable      "MSIE [1-6]\.(?!.*SV1)";
  gzip_vary         on;
  gzip_types        text/plain application/xml text/css text/javascript     image/svg+xml image/x-icon application/javascript application/x-javascript;
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

server {
  gzip              on;
  gzip_disable      "MSIE [1-6]\.(?!.*SV1)";
  gzip_vary         on;
  gzip_types        text/plain application/xml text/css text/javascript image/svg+xml image/x-icon application/javascript application/x-javascript;
  gunzip            on;

  listen        443 ssl;
  server_name   ${DOMAIN} www.${DOMAIN};

  ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

  include     /etc/nginx/options-ssl-nginx.conf;

  ssl_dhparam /vol/proxy/ssl-dhparams.pem;

  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

  location /static {
    alias /vol/static;
    gzip_static on;
  }

  location / {
      uwsgi_pass           ${APP_HOST}:${APP_PORT};
      include              /etc/nginx/uwsgi_params;
      client_max_body_size 10M;
  }
}