FROM python:3.10-alpine3.16
ENV PYTHONUNBUFFERED 1
# Abychom mohli spouštět scripty
ENV PATH="/scripts:$PATH"
# Přeopírování scriptů
COPY ./scripts /scripts

# Vytvoření nového uživatele + změna ownera složky pro static files
RUN addgroup app && adduser -S -G app app
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/price-list
RUN chown -R app:app /vol
# uživatel, který vlastní složku bude mít full přístup a ostatní jen read
RUN chmod -R 755 /vol/web
# Povolíme spouštění scriptů
RUN chmod +x /scripts/entrypoint.sh
# Balíčky potřebné pro uwsgi
RUN apk add --upgrade --no-cache build-base linux-headers && \
  pip install --upgrade pip

# Určíme prac. složku + překopírujeme vše potřebné a spustíme instalaci knihoven, které budu potřebovat
WORKDIR /app
COPY requirements.txt .
RUN  pip install -r /app/requirements.txt
COPY web/ .

USER app
# Vyhodnotí tento script, který obsahuje příkazy pro spuštění aplikace
# Je to kvůli tomu, že budeme startovat uWSGI a ten spustí naši aplikaci
CMD ["entrypoint.sh"]