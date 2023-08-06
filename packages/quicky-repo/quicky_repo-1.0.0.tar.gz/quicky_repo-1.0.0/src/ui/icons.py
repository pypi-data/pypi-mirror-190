"""
  This class is an enum that represents icons [+], [-] and [?].
  Needs RICH module (https://pypi.org/project/rich)
"""
from enum import Enum

class Icon(Enum):
  PLUS = '[green][[/green]+[green]][/green]'
  MINUS = '[red][[/red]-[red]][/red]'
  INTERROGATIVE = '[yellow][[/yellow]?[yellow]][/yellow]'
