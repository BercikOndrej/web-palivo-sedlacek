# Website palivosedlacek.cz

## Technologies
- Python + Django
- uWSGI (application server)
- Nginx (proxy server)
- Certbot (for free https certificate)
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
        - manage files and text compression
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
    - Here in script we must be careful -> we need specify both `DOMAIN` names: `-d "www.$DOMAIN"` and also `-d "$DOMAIN"`

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
    - Put the key into `Settings > Deploy Keys`

10. Now we can clone our project to our server

11. After cloning we can get our first certificate
    - `docker-compose run --rm certbot /opt/certify-init.sh` -> start certbot to get and download our certificate
    - `BE CAREFUL`: We cannot requesting certificate more then 5x for the same domain in 168 hours
    - After that container ends and our certificate is ready for use

12. Then we need start our app via HTTPS
    - `docker-compose down`
    - `docker-compose up`
    - Now is our app ready

13. Handling renewals
    - The steps above will create an initial certificate for our project. However, the certificate will only be valid for three months, so you’ll need to run the renew command before then
    - `docker-compose run --rm certbot sh -c "certbot renew"` for renew certificate
    - For automation renew  we need use tool like `cron`
    - We have template for `renew.sh` script in directory `scripts` which one we must edit
    - And then allowed perrmission `chmod +x renew.sh`:

  ```
  #!/bin/sh
  set -e

  cd <path_to_project_folder>
  docker-compose run --rm certbot certbot renew
  ```

14. Afterthat we must specify by tool `cron` to execute this script repeatedly at a given time
    - `crontab -l` -> display list of all cron jobs
    - `crontab -e` -> edit cron  jobs
    - We need to add `0 0 * */ * sh <path_to_renew.sh>` to renew certificate automaticaly
    - For example `0 0 * */ * sh /root/renew.sh` to renew certificate every month
    - For example `0 0 * * 6 sh /root/renew.sh` for weekly renew at midnight 


## App edit
- We can edit our app localy and then push changes into Github repo
- Then we need redeploy app again -> Clone repository and deploy app

### Price list edit/change
- We can do that by `SCP (Secure copy)`
- `scp <file> <user>@<server_ip_address>:<absolute_path_to_old_price-list>`
- For example: `scp Cenik.csv root@64.226.69.165 /root/web-palivosedlacek/data/Cenik.csv`
- New price list file must be named exatly `Cenik.csv`
- It is posible because of volume definition in `docker-compose.yml` file for our service `app` : `./data:/vol/web/price-list` -> app always take price list from `data` directory
- We need always turn off out website containers and then start up again

## Others staff I don`t know about

### Open Graph Meta Tags (OG tags)
- These tags provides more visibility and more attention on social media like Twitter, Facebook, LinkedIn and others
- Tags control how urls are displayed on social media
- We can find them in `<head>` section of website with `og` prefix
- Tags are so important
    - They make website url more clickable and readable
    - Tell people about website content
    - They help Facebook understand what the content of website is about -> again better result in researching
    - Also people may sharing your url as good-looking post on their social media
- Official [OG tags documentation] describes all posible og tags to use
- I follow [best practices for using og tags](https://ahrefs.com/blog/open-graph-meta-tags/) 

### Google Search Console
- Before this we must have good SEO score 
- We need do this because without it, our website doesn't appeaer in Google search
- To test if our website is visible for google searching is write `site:<our-domain>` into searching panel on google

1. Step - Verify website ownership in `Google Search Console`
    - It is done by `TXT` records
    - Google Search Console generetes TXT records for us and we must put them into our DNS configuration of our domain

2. Step - Index the page you want to appear in Google Search
    - In our Google Search Console settings we must do `url inspection` where we place our website's url
    - Then we request Google for indexing our page
    - This take some time so we has to wait for Google

- After that we can test visibility of our website in Google searching

### Add website icon
- We need have right format of icon -> `favicon.ico` is the best options but more formats is supported
- We can create a favicon on [favicon.io](https://favicon.io)
- We need define path to our favicon in `header` html section:
`<link rel="icon" type="image/ico" href="{% static 'website/favicon.ico' %}">`
- If we don't see any changes we can try empty cashes of web browser
- We can see changes after reindexing our website inn Google searching result

### Add backlinks in our (borthers) Google company/business website

### Adding more keywords
- We need a lots of words for good searching result of our website
- We can include names of products too

### Give reading permmisson to UI bots for better research results
- We must specify file `robots.txt` that say our website is readable by UI bots
- This file must be available on url `our-domain/robots.txt`
- Example `palivosedlacek.cz/robots.txt`
- In our case we defined this by django `url` and `views` pattern

### Enable gzip and gunzip on proxy nginx
- It is for compress and uncompress text, files and others
- For our purpose we need just text compression and static files compression -> In our nginx config files `default-ssl.conf.tpl` and `default.conf.tpl` we inserted:
```
server {
  gzip              on;
  gzip_disable      "MSIE [1-6]\.(?!.*SV1)";
  gzip_vary         on;
  gzip_types        text/plain application/xml text/css text/javascript image/svg+xml image/x-icon application/javascript application/x-javascript;
  gunzip            on;
  
  ...
  ...
  ...

  location /static {
    alias /vol/static;
    gzip_static on;
  }
}
```