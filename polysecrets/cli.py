import click, sys
from polysecrets.main import PolySecrets
from polysecrets.version import __version__

_def_sec = 'HOXubh876Gv66v845345FTfhmd'
def go(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'Secret: {PolySecrets(config).manual()}')
    ctx.exit()


@click.command()
@click.argument('go', nargs=1, type=click.UNPROCESSED)
@click.option('-s', '--secret', required=False, default=_def_sec, type=click.STRING, help='The secret string')
@click.option('-l', '--length', default=10, type=click.INT, help='Length of the secret. Secret has a minimum length '
                                                                 'of 10')
@click.option('-i', '--interval', default=30, type=click.INT, help='How frequently should a new secret be generated '
                                                                   '(in seconds)')
@click.option('-u', '--uuid', default='yes', type=click.STRING, help='Whether to use UUIDs or Alphanumeric characters for '
                                                                 'secret generation - yes, no, both')
@click.option('-m', '--mixcase', default=False, type=click.BOOL, help='Decide whether or not to mix the case of alpha'
                                                                      'characters in secret string')
@click.option('-p', '--persist', default=False, type=click.BOOL, help='Never get the same secret twice with '
                                                             'persistence from MongoDB. A .env file is required.')
@click.option('--symbols', default=False, type=click.BOOL, help='Whether or not to use special characters in secret. This will only increase the probability of appending a special character.')                                                          
@click.version_option(version=__version__)
def cli(go, secret, length, interval, uuid, mixcase, persist, symbols):
    if not isinstance(uuid, str):
        print(f'UUID must equal True, False or "Both". You have {uuid}, which is invalid.')
        sys.exit()

    config = dict(
        secret=secret,
        length=length,
        interval=interval,
        uuid=uuid,
        mixcase=mixcase,
        symbols=symbols,
        persist=persist
    )
    click.echo(f'Secret: {PolySecrets(config).manual()}')


if __name__ == '__main__':
    try:
        cli()
    except (AttributeError, AssertionError, TypeError) as excep:
        print(f'Fatal error - {excep}')
        sys.exit(1)
