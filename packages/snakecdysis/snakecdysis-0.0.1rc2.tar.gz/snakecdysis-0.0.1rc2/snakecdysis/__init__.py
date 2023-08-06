from pathlib import Path
from .snake_wrapper import SnakEcdysis, SnakeInstaller
from .cli_wrapper import main_wrapper
from .useful_function import *


__version__ = Path(__file__).parent.resolve().joinpath("VERSION").open("r").readline().strip()

__doc__ = """
:author: Sebastien Ravel
:contact: sebastien.ravel@cirad.fr
:date: 01-01-2023
:version: """ + __version__ + """

You want to wrap your best snakemake workflow to be easy install and run, Snakecdysis is for you !!!!!
Tha aim of Snakecdysis is to easy-wrapped snakemake workflow as python package and then build sub-commands to manage this.
"""
