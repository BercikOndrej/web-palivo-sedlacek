# Website palivosedlacek.cz

## Technologies
- Python + Django
- uWSGI (application server)
- nginx (proxy server)
- certbot (for free https certificate)
- Docker
- HTML + CSS (frontend)

## App deployment
- By tutorial on [blog](https://londonappdeveloper.com/django-docker-deployment-with-https-using-letsencrypt/) (also [youtube video](https://www.youtube.com/watch?v=3_ZJWlf25bY&t=4785s) is available)
- Hosting server is droplet in [DigitalOcean](https://www.digitalocean.com).
- Domain is from [Můj Český hosting](https://muj.cesky-hosting.cz/login.php)


1. Define requirements.txt file
    - This file contains a list of all Python requirements out project needs
    - [requirements.txt](requirements.txt)

2. Create Dockerfile for out django app
    - We assume we already have a working project using production server `uWSGI`
    - Whole django app is in the `web` folder
    - Django project must be prepare for production -> changes in [settings.py](web/web/settings.py)
    - This file defining a start script `scripts/entrypoint.sh`
    - [Django Dockerfile](Dockerfile)

3. Create Nginx reverse proxy server
    - We must specify creation of nginx proxy server in folder `docker/proxy/` that:
        - serves static files
        - redirect HTTP request to HTTPS
        - forwards requests to uWSGI
    - We must create several config files:
        - [default.conf.tpl](docker/proxy/nginx/default.conf.tpl)
        - [default-ssl.conf.tpl](docker/proxy/nginx/options-ssl-nginx.conf)
        - [uwsgi_params](docker/proxy/nginx/uwsgi_params) provided by nginx official site -> we must just copy a file and insert in our project
        - [options-ssl-nginx.conf](docker/proxy/nginx/options-ssl-nginx.conf) available in [certbot github](https://github.com/certbot/certbot/blob/1.28.0/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf). Again copy and insert into project.
    - We also need [Dockerfile](docker/proxy/Dockerfile) for our nginx
    - Last we need create start script [run.sh](docker/proxy/run.sh) 

4. Create Certbot for retrieve our first free certificate for HTTPS
    - Certbot will be in `docker` folder same as `proxy`
    - And also we need create [Dockerfile](docker/certbot/Dockerfile) and start script [certify-init.sh](docker/certbot/certify-init.sh)

5. Then we need put all together in [docker-compose.yml](docker-compose.yml)
    - Here we set variables like:
        - `DOMAIN`
        - `EMAIL_SETTING`
        - `SECRET_KEY`
    - Also we need specify correctly all `volumes` for certbot, static files and others

6. In this stage we need create github repo and push all code there because we will need clone the code into the server

7. Then we need set `hosting server` (DigitalOcean droplet) and our `domain`
    - More info for droplet creation and for connect to the server in `Notes` 
    - More info for domain creation and redirect domain to the server in `Notes`

8. After getting server we need install `Docker` and `Docker-compose` for running our app
    - We use official tutorials for `Ubuntu`
    - In the end of installation try `hello-word image`

9. Before deployment from Github repo we must create `deploy key` on server and configure our Github project to permit cloning with this key
    - `ssh-keygen -t ed25519 -C "GitHub Deploy Key"`
    - `cat ~/.ssh/id_ed25519.pub` and copy the key into the clipboard
    - put the key into `Settings > Deploy Keys`

10. Now we can clone our project to our server

11. After cloning we can get our first certificate
    - `docker-compose run --rm certbot /opt/certify-init.sh` -> start certbot to get and download our certificate
    - after that container ends and our certificate is ready for use

12. Then we need start our app via HTTPS
    - `docker-compose down`
    - `docker-compose up`
    - Now is our app ready

13. Handling renewals
    - The steps above will create an initial certificate for our project. However, the certificate will only be valid for three months, so you’ll need to run the renew command before then
    - `docker-compose run --rm certbot sh -c "certbot renew"` for renew certificate
    - For automation renew  we need use tool like `cron`
    - We create `renew.sh` script in the home directory of server user `(/home/<user>/renew.sh, for us: /root)` (script will be store in priject folder `scripts`) and then allowed perrmission `chmod +x renew.sh`:

  ```
  #!/bin/sh
  set -e

  cd /home/<user>/<project_name>
  /usr/local/bin/docker-compose --rm certbot certbot renew
  ```

14. Afterthat we must specify by tool `cron` to execute this script repeatedly at a given time
    - `crontab -l` -> display list of all cron jobs
    - `crontab e` -> edit cron  jobs
    - We need to add `0 0 * */ * sh /root/renew.sh` to renew certificate every month
    - or for example `0 0 * * 6 sh /root/renew.sh` for weekly renew at midnight 


## App edit
- We can edit our app localy and then push  changes into Github repo
- Then we need redeploy app again -> Clone repository and deploy app
- When 