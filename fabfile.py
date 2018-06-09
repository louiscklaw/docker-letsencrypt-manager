#!/usr/bin/env python

import os
import sys

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

CWD = os.path.dirname(__file__)
PROJ_HOME = [CWD, '/srv/docker-files/docker-letsencrypt-manager']



def send_to_gcp():
    exclude_string = ' '.join(['--exclude {}'.format(exclude_item) for exclude_item in [
        '__pycache__','.git','*.log','tmp','temp','*.pyc'
    ]])
    rsync_project(
        local_dir=PROJ_HOME[0] + '/',
        remote_dir=PROJ_HOME[1],
        exclude=['__pycache__','.git','*.log','tmp','temp','*.pyc'],
        delete=True,
        extra_opts='--recursive'
    )

def docker_compose_pull():
    with cd(PROJ_HOME[1]):
        run('docker-compose pull')

def destroy_proj_dir():
    with settings(warn_only=True):
        run('rm -rf {}'.format(PROJ_HOME[1]))

def recreate_proj_dir():
    with settings(warn_only=True):
        run('mkdir -p {}'.format(PROJ_HOME[1]))

def destroy_recreate():
    destroy_proj_dir()
    recreate_proj_dir()

@task
@hosts(['logic@aboutme.louislabs.com'])
def build_on_gcp():
    destroy_recreate()
    send_to_gcp()
    docker_compose_pull()
