import click, sys
from polysecrets.main import PolySecrets
from polysecrets.version import __version__


@click.command()
@click.option('-s', '--secret', type=click.STRING, help='The secret string')
@click.option('-l', '--length', default=10, type=click.INT, help='Length of the secret. Secret has a minimum length '
                                                                 'of 10')
@click.option('-u', '--uuid', default=True, type=click.INT, help='Whether to use UUIDs or Alphanumeric characters for '
                                                                 'secret generation')
@click.option('-m', '--mixcase', default=False, type=click.BOOL, help='Decide whether or not to mix the case of alpha'
                                                                      'characters in secret string')
@click.option('-p', '--persist', default={}, type=dict, help='Never get the same secret twice with '
                                                             'persistence from MongoDB')
@click.version_option(version=__version__)
def cli(secret, length, interval, uuid, mixcase, persist):
    if not isinstance(uuid, bool) or uuid is not 'Both':
        print(f'UUID must be a True, False or Both. You have {uuid}, which is invalid.')
        sys.exit()

    config = dict(
        secret=secret,
        length=length,
        interval=interval,
        uuid=uuid,
        mixcase=mixcase,
        persist=persist
    )
    print('Secret: ', PolySecrets(config).manual())
    sys.exit()


if __name__ == '__main__':
    try:
        cli()
    except (AttributeError, AssertionError, Exception) as excep:
        print(f'Fatal error - {excep}')
        sys.exit(1)
