#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers using do_deploy function
"""

from fabric.api import *
import os.path

env.hosts = ['18.209.178.99', '54.157.165.107']
env.user = 'ubuntu'
env.key_filename = '/alx-system_engineering-devops/0x0B-ssh/school.pub'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p /data/web_static/releases/{}".format(archive_no_ext))

        with cd("/data/web_static/releases/{}".format(archive_no_ext)):
            run("tar -xzf /tmp/{} -C .".format(archive_name))

        run("rm /tmp/{}".format(archive_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -f /data/web_static/current")

        # Create a new symbolic link /data/web_static/current linked to the new version
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_no_ext))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False

