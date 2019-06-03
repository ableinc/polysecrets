import click, sys
from polysecrets.main import PolySecrets
from polysecrets.version import __version__


@click.command()
@click.option('-s', '--secret', required=1, type=click.STRING, help='The secret string')
@click.option('-a', '--automate', default=False, type=click.BOOL, help='Automate the secret generation process. '
                                                                       'This adds to secret to your environment '
                                                                       'under "secret"')
@click.option('-t', '--time', default=30, type=click.INT, help='Number of seconds until new secret is created.')
@click.version_option(version=__version__)
def cli(secret, automate, time):
    if automate:
        PolySecrets(secret, time).automated()
        sys.exit()
    else:
        print('Secret: ', PolySecrets(secret).manual())
        sys.exit()


if __name__ == '__main__':
    try:
        cli()
    except (AttributeError, AssertionError, Exception) as excep:
        print(f'Fatal error - {excep}')
        sys.exit(1)
