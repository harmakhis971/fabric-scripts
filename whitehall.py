from fabric.api import task, hosts, sudo, cd, execute


@task
def dedupe_stats_announcement_from_file(filename):
    """De-duplicate Whitehall statistics accouncements from a CSV file"""
    with open(filename) as fd:
        duplicates = [line.strip().split(',') for line in fd]
        for duplicate_slug, authoritative_slug in duplicates:
            execute(
                dedupe_stats_announcement, duplicate_slug, authoritative_slug)


@task
@hosts('whitehall-backend-1.backend')
def dedupe_stats_announcement(duplicate_slug, authoritative_slug, noop=False):
    """De-duplicate Whitehall statistics announcement"""
    noop = bool(noop)
    command = 'govuk_setenv whitehall ./script/dedupe_stats_announcement'
    if noop:
        command += ' -n'
    command += ' {} {}'.format(duplicate_slug, authoritative_slug)
    with cd('/var/apps/whitehall'):
        sudo(command, user='deploy')


@task
@hosts('whitehall-backend-1.backend')
def unarchive_content(*edition_ids):
    """Unarchive Whitehall content"""
    command = 'govuk_setenv whitehall bundle exec rake unarchive_edition[{}]'
    with cd('/var/apps/whitehall'):
        for edition_id in edition_ids:
            sudo(command.format(edition_id), user='deploy')
