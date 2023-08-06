import os
import json
from pathlib import Path

class Command:
    """
        Command Interface
    """

    BULK_CONFIG_PATH = os.path.join(os.getcwd(), 'bulk.json')
    DEFAULT_CONFIG_PATH = os.path.join(Path(__file__).parent.parent, 'bulk_python', 'configs' , 'default.json')

    @staticmethod
    def config() -> dict:
        """
            returns project config file or default config
        """
        path = __class__.BULK_CONFIG_PATH if Path(
            __class__.BULK_CONFIG_PATH).exists() else __class__.DEFAULT_CONFIG_PATH

        with open(path, 'rb') as file:
            return json.loads(file.read())

    def run(self):
        """
            Your run middleware here
        """
        raise NotImplementedError

    def execute(self):
        """
            command is called
        """
        return self.run()
