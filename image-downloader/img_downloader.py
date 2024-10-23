import click


@click.command()
@click.argument('url', nargs=1, type=click.STRING)
def imget(url):
    click.echo(f'{url}')
