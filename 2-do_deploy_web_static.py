#!/usr/bin/python3
"""
Fabric script that generate a .tgz archive
"""
from fabric.api import *


def do_pack():
    """
    Generate the .tgz archive
    """
    from datetime import datetime
    import os.path

    today = datetime.now()

    tgz_file_path = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(
            today.year, today.month,
            today.day, today.hour,
            today.minute, today.second
    )

    if not os.path.exists('versions'):
        os.mkdir('versions')

    print('Packing web_static to ' + tgz_file_path)
    res = local('tar  -cvzf {} {}'.format(
        tgz_file_path, 'web_static')
    )

    if res.stderr:
        return None

    file_stats = os.stat(tgz_file_path)

    print('web_static packed: {} -> {}Bytes'.format(
        tgz_file_path, file_stats.st_size)
    )

    if not res.stderr:
        return os.path.realpath(tgz_file_path)
    else:
        return None


def do_deploy(archive_path):
    """
    Deploy web_static archive on servers
    """
    import os.path

    if not os.path.exists(archive_path):
        return None

    env.hosts = ['52.3.245.71', '54.175.98.56']

    env.username = 'ubuntu'

    remote_archive = '/tmp/' + os.path.basename(archive_path)

    remote_folder = '/data/web_static/releases/'
    remote_folder += os.path.splitext(os.path.basename(archive_path))[0]

    put(local_path=archive_path, remote_path=remote_archive)

    r = sudo('mkdir -p {} && tar -xvf {} -C {}'.format(
        remote_folder, remote_archive, remote_folder)
    )
    if r.stderr:
        return False

    r = sudo('rm ' + remote_archive)
    if r.stderr:
        return False

    sudo('rm -f /data/web_static/current')
    sudo('ln -sf {} {}'.format(
        remote_folder + '/web_static',
        '/data/web_static/current')
    )

    return True
