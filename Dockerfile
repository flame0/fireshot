FROM ubuntu:latest
MAINTAINER Andrew Lee

RUN apt-get update && apt-get install -y \
    git \
    vim \
    python3 \
    python3-pip \
    nginx \
    supervisor \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    pwgen && rm -rf /var/lib/apt/lists/*
RUN pip3 install uwsgi

ADD . /app
ENV HOME /app
WORKDIR /app
EXPOSE 80
# nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY django_nginx.conf /etc/nginx/sites-available/default

# supervisor config
COPY supervisor.conf /etc/supervisor/conf.d/

CMD ["/bin/bash", "/app/docker-entrypoint.sh"]
