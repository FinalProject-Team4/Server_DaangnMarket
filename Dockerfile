# daangnMarket api
FROM        python:3.7-slim

RUN         apt-get -y -qq update && \
            apt-get -y -qq dist-upgrade && \
            apt-get -y -qq autoremove

# Nginx, gettext, npm 설치
RUN         apt-get -y -qq install nginx && \
            apt-get -y -qq install binutils libproj-dev gdal-bin && \
            rm -rf /var/lib/apt/lists/* && \
            apt-get clean

# install packages
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt


# 소스코드 복사
COPY        ./app /srv/daangn-market/app
WORKDIR     /srv/daangn-market/app


# config 파일 복사(nginx, gunicorn, supervisor)
COPY        ./.config ../.config

# Nginx설정파일 링크, 기본 서버 설정 삭제
RUN         rm /etc/nginx/sites-enabled/default
COPY        .config/daangn-market.nginx /etc/nginx/sites-available
RUN         ln /etc/nginx/sites-available/daangn-market.nginx /etc/nginx/sites-enabled/daangn-market.nginx

# gunicorn 로그폴더 생성
RUN         mkdir /var/log/gunicorn

CMD         /bin/bash
