import sys

import pkg_resources

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
                return InstallCommand(['--install-single'], {'package': argv[1]})
        else:
            return InstallCommand(['--install-all'])
    elif 'run' in argv:
        if len(argv) > 1:
            return RunCommand({'script': argv[1]})
        else:
            return RunCommand()
    elif 'init' in argv:
        if '--ancestor=pip' in argv:
            return InitCommand({'ancestor': 'pip'})
        else:
            return InitCommand()
    else:
        print(f"""
            Bulk (version { pkg_resources.get_distribution('bulk_python').version })
            
            Usage:
                command [options] [arguments]

            Options:
            --dry            add dependencies without install from pip
            --ancestor       Provide previous install (Default bulk) (Choice pip or bulk)


            Available commands:
                init               Creates a basic bulk.json file in the current directory.
                install            Installs the project dependencies.
        """)


def cli(args: list = None):
    """
        main application function
    """
    if not args:
        args = sys.argv

    command = commands(args[1:])
    if command:
        command.run()


if __name__ == '__main__':
    cli()
