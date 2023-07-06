#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['18.209.178.99', '54.157.165.107']
env.user = 'ubuntu'
env.key_filename = '/alx-system_engineering-devops/0x0B-ssh/school.pub'


def do_pack():
    """Creates a compressed archive of the web_static folder"""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_path = "versions/web_static_{}.tgz".format(now)
        local("tar -czvf {} web_static".format(file_path))
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_file = archive_path.split('/')[-1]
        archive_folder = "/data/web_static/releases/{}".format(archive_file[:-4])
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_file, archive_folder))

        # Move files out of the archive folder
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))
        run("rm -rf {}/web_static".format(archive_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_file))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current linked to the new version of your code
        run("ln -s {} /data/web_static/current".format(archive_folder))

        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

