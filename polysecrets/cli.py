import click, sys
from polysecrets.main import PolySecrets
from polysecrets.version import __version__


def go(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    config = {}
    click.echo(f'Secret: {PolySecrets(config).manual()}')
    ctx.exit()


@click.command()
@click.argument('go', nargs=1, type=click.UNPROCESSED)
@click.option('-s', '--secret', required=False, default='rAnd0m_s3cr3t+', type=click.STRING, help='The secret string')
@click.option('-l', '--length', default=10, type=click.INT, help='Length of the secret. Secret has a minimum length '
                                                                 'of 10')
@click.option('-i', '--interval', default=30, type=click.INT, help='How frequently should a new secret be generated '
                                                                   '(in seconds)')
@click.option('-u', '--uuid', default='True', type=click.STRING, help='Whether to use UUIDs or Alphanumeric characters for '
                                                                 'secret generation')
@click.option('-m', '--mixcase', default=False, type=click.BOOL, help='Decide whether or not to mix the case of alpha'
                                                                      'characters in secret string')
@click.option('-p', '--persist', default={}, type=dict, help='Never get the same secret twice with '
                                                             'persistence from MongoDB')
@click.version_option(version=__version__)
def cli(go, secret, length, interval, uuid, mixcase, persist):
    if not isinstance(uuid, str):
        print(f'UUID must equal True, False or "Both". You have {uuid}, which is invalid.')
        sys.exit()

    config = dict(
        secret=secret if go is False else 'rAn!d0m_@s3cr#3t+',
        length=length,
        interval=interval,
        uuid=uuid,
        mixcase=mixcase,
        persist=persist
    )
    click.echo(f'Secret: {PolySecrets(config).manual()}')


if __name__ == '__main__':
    print('Experimental v0.1.3')
    try:
        cli()
    except (AttributeError, AssertionError, TypeError) as excep:
        print(f'Fatal error - {excep}')
        sys.exit(1)
