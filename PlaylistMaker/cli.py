import click
from playlistmaker import *

@click.command()
@click.argument('term', default=None, required=False)
def main(term):
  if term == None:
    click.echo("You must provide some text to search!")
  else:
    results = playlistmaker(term)
    for result in results:
      click.echo(result)
      click.echo("\n")
