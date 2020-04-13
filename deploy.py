#!/usr/bin/env python
import json
import os
import subprocess
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

HOME = str(Path.home())
PROJECT_NAME = 'daangn-market'
PROJECT_DIR = os.path.dirname(ROOT_DIR)
PROJECT_DIR = os.path.join(ROOT_DIR, PROJECT_NAME, 'Server_DaangnMarket_Fork')
SECRETS_FILE = os.path.join(PROJECT_DIR, 'secrets.json')

USER = 'ubuntu'
HOST = json.load(open(SECRETS_FILE))['HOST']
TARGET = f'{USER}@{HOST}'
EC2_CERT = os.path.join(HOME, '.ssh', f'daangnMarket.pem')

DOCKER_IMAGE = f'newjam/{PROJECT_NAME}'
DOCKER_IMAGE_TAG = 'test'
DOCKER_OPTS = [
    ('--rm', ''),
    ('-t', ''),
    ('-d', ''),
    ('-p', '80:80'),
    # ('-p', '443:443'),
    # ('-v', '/etc/letsencrypt:/etc/letsencrypt'),
    ('--name', PROJECT_NAME),
]


# LOCAL bash command
def run(cmd, check_error=False):
    subprocess.run(cmd, shell=True, check=check_error)


# EC2 bash command
def ssh_run(cmd, check_error=True, host_key_check=False):
    strict_host_key_check = f'-o StrictHostKeyChecking=no' if not host_key_check else ''
    run(f'ssh {strict_host_key_check} -i {EC2_CERT} {TARGET} -C {cmd}', check_error)


# Docker Container command
def docker_run(cmd, container=PROJECT_NAME, daemon=False, check_error=True, host_key_check=False):
    ssh_run(f'\' sudo docker exec {"-d" if daemon else ""} {container} {cmd} \'', check_error, host_key_check)


# docker build, push from LOCAL
def local_build_push():
    run(f'poetry export --dev -f requirements.txt > requirements.txt')
    run(f'docker build -q -t {DOCKER_IMAGE}:{DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE}:{DOCKER_IMAGE_TAG} | grep -e push -e digest')


# server init from EC2
def server_init():
    ssh_run(f'sudo apt-get update -y > /dev/null')
    ssh_run(f'sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y > /dev/null')
    ssh_run(f'sudo apt-get install docker.io -y -qq')


# docker server run from EC2 : docker pull, run
def server_run():
    ssh_run(f'sudo docker stop {PROJECT_NAME}', check_error=False)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE}:{DOCKER_IMAGE_TAG} | grep -e "Pulling from" -e Digest -e Status')
    ssh_run('sudo docker run {options} {img}:{tag}'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTS
        ]),
        img=DOCKER_IMAGE,
        tag=DOCKER_IMAGE_TAG,
    ))


# copy secrets from LOCAL: local to EC2, EC2 to docker
def copy_secrets():
    # secrets.json
    run(f'scp -i {EC2_CERT} {SECRETS_FILE} {TARGET}:/tmp')
    ssh_run(f'sudo docker cp /tmp/secrets.json {PROJECT_NAME}:/srv/{PROJECT_NAME}')
    # serviceAccountKey.json
    run(f'scp -i {EC2_CERT} serviceAccountKey.json {TARGET}:/tmp')
    ssh_run(f'sudo docker cp /tmp/serviceAccountKey.json {PROJECT_NAME}:/srv/{PROJECT_NAME}')
    # HTTPS
    # run(f'scp -i {EC2_CERT} -r .cert {TARGET}:/tmp/.cert')
    # ssh_run(f'sudo docker cp -a /tmp/.cert {PROJECT_NAME}:/srv/{PROJECT_NAME}/.cert')


# set prerequisites from docker CONTAINER
def server_setting():
    # stop nginx
    docker_run(f'/usr/sbin/nginx -s stop', check_error=False)

    # collect static files
    docker_run(f'python manage.py collectstatic --noinput')

    # database migrate
    # docker_run(f'python manage.py migrate > /dev/null')

    # start supervisor
    docker_run(f'supervisord -c /srv/daangn-market/.config/supervisord.conf -n', daemon=True)


if __name__ == '__main__':
    try:
        print(">>>>> local_build_push()")
        local_build_push()
        print(">>>>> server_init()")
        server_init()
        print(">>>>> server_run()")
        server_run()
        print(">>>>> copy_secretes()")
        copy_secrets()
        print(">>>>> server_setting()")
        server_setting()
    except subprocess.CalledProcessError as e:
        print(' deploy.py Error!')
        print(' cmd:', e.cmd)
        print(' return code:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)
