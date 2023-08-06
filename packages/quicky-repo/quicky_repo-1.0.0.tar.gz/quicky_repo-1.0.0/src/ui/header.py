from core.settings import settings
from rich.panel import Panel
from pyfiglet import figlet_format

fast_repo = figlet_format('Fast Repo')
header = Panel.fit(f'[bold yellow]{fast_repo}', title=f'[cyan]{settings.version}')
