import sys

from .run import RunCommand
from .init import InitCommand
from .install import InstallCommand

def commands(argv: list):
    """
        Switch command
    """
    if 'install' in argv:
        if len(argv) > 1:
            if argv[1] == '--dry':
                return InstallCommand(['--dry'])
            else:
                return InstallCommand(['--install-single'], { 'package': argv[1] })
        else:
            return InstallCommand(['--install-all'])
    elif 'run' in argv:
        if len(argv) > 1:
            return RunCommand({ 'script': argv[1] })
        else:
            return RunCommand()
    elif 'init' in argv:
        if '--ancestor=pip' in argv:
            return InitCommand({ 'ancestor': 'pip' })
        else:
            return InitCommand()

def cli(args: list = None):
    """
        main application function
    """
    if not args:
        args = sys.argv

    command = commands(args[1:])
    command.run()

if __name__ == '__main__':
    cli()
