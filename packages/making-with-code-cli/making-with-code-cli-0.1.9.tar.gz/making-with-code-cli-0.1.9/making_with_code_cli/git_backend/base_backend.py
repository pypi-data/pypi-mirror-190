from pathlib import Path
from subprocess import run, CalledProcessError
import click
from making_with_code_cli.helpers import cd
from making_with_code_cli.cli_setup import WORK_DIR_PERMISSIONS
from making_with_code_cli.styles import (
    address,
    confirm,
    error,
)

class GitBackend:
    """Base class interface to backend git server.
    All Making With Code deployments are backed by a git server, but the nature of the
    server and the strategies for completing tasks vary by backend. 
    """
    INIT_ACTIONS = [
        'create_from_template',
        'clone',
        'mkdir'
    ]

    @classmethod
    def extend_settings(self, settings):
        "A hook for git backends to collect additional information from the user"
        return settings

    def __init__(self, settings):
        self.settings = settings

    def init_module(self, module, modpath):
        if not 'init_action' in module:
            raise ValueError(f"There is a problem with the website. Can't initialize module {module['slug']} " + 
                    "without an init action.")
        if not module['init_action'] in self.INIT_ACTIONS:
            raise ValueError(f"There is a problem with the website. Can't initialize module {module['slug']} " + 
                    f"with init action '{module['init_action']}'.")
        if module['init_action'] == "mkdir":
            self.init_mkdir(module, modpath)
        if module['init_action'] == "clone":
            self.init_clone(module, modpath)
        if module['init_action'] == "create_from_template":
            self.init_create_from_template(module, modpath)

    def init_mkdir(self, module, modpath):
        modpath.mkdir(mode=WORK_DIR_PERMISSIONS)

    def init_clone(self, module, modpath):
        raise NotImplemented()

    def init_create_from_template(self, module, modpath):
        raise NotImplemented()

    def update(self, module, modpath):
        if (modpath / ".git").is_dir():
            with cd(modpath):
                relpath = self.relative_path(modpath)
                try:
                    click.echo(address(f"Checking {relpath} for updates.", preformatted=True))
                    run("git pull", shell=True, check=True)
                    if Path("pyproject.toml").exists():
                        run("poetry update", shell=True, check=True)
                except CalledProcessError as e:
                    click.echo(error(f"There was a problem updating {relpath}. Ask a teacher."))
                    raise e

    def work_dir(self):
        return Path(self.settings['work_dir'])

    def relative_path(self, path):
        return path.relative_to(self.work_dir())

