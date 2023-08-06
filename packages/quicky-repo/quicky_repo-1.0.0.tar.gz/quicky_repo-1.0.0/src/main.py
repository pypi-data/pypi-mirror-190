import click
from core.settings import settings
from commands.init import init

@click.version_option(settings.version, message='Fast Repo version %(version)s')
@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
  """
    ⚡ Initialize your projects as fast as you want.
  """
  pass

if __name__ == '__main__':
  cli.add_command(init)
  cli()
