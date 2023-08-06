from pathlib import Path

from .command import Command
from .install import InstallCommand


class InitCommand(Command):
    """
        Init bulk in project
    """

    def __init__(self, params: dict = None):
        self.params = params if params else {'ancestor': 'bulk'}

    def run(self):
        path = Path('requirements.txt')

        install = InstallCommand(options=[])
        can_install = self.params.get('ancestor') != 'bulk' or path.exists()
        install.lock(can_install, self.params.get('ancestor'))
