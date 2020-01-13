import puppet
from fabric.tasks import task

maintenance_config = '/etc/nginx/includes/maintenance.conf'


@task
def enable_maintenance(context):
    """Enables a maintenance page and serves a 503"""
    """Only to be run on loadbalancers"""
    if not fabric.contrib.files.exists(maintenance_config):
        abort("Sorry this task can only currently be run on loadbalancers")
    puppet.disable("Maintenance mode enabled")
    sudo("echo 'set $maintenance 1;' > {0}".format(maintenance_config))
    sudo('service nginx reload')


@task
def disable_maintenance(context):
    """Disables a maintenance page"""
    """Only to be run on loadbalancers"""
    if not fabric.contrib.files.exists(maintenance_config):
        abort("Sorry this task can only currently be run on loadbalancers")
    sudo("echo 'set $maintenance 0;' > {0}".format(maintenance_config))
    sudo('service nginx reload')
    puppet.enable()


def gracefulstop(context, wait=True):
    """Gracefully shutdown Nginx by finishing any in-flight requests"""
    sudo('nginx -s quit')

    if wait:
        # Poll for Nginx, until it's no longer running.
        run('while pgrep nginx >/dev/null; do echo "Waiting for Nginx to exit.."; sleep 1; done')


@task
def gracefulrestart(context):
    """Gracefully shutdown and start Nginx (not reload)"""
    gracefulstop()
    start()


@task
def kill(context):
    """Shut down Nginx immediately without waiting for it to finish running"""
    sudo('service nginx stop')


@task
def start(context):
    """Start up Nginx on a machine"""
    sudo('service nginx start')


@task
def force_restart(context):
    """Turns Nginx off and on again"""
    kill()
    start()
