import click
from subprocess import Popen
from rich import print
from ui.icons import Icon

@click.command()
def init():
  """Initialize a project with the best boilerplate"""
  print(f'{Icon.INTERROGATIVE.value} Looking for available boilerplates...')
  print('[b green]Found!')

  Popen(['git', 'clone', 'https://github.com/kauefraga/server-structure.git', 'backend_boilerplate']).wait()
