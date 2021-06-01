import sys
import click

from src.click_context import cli
from src.module_indexing import kmers as index_kmers       # pylint: disable=relative-beyond-top-level



cli.add_command(index_kmers, name="index")


if __name__ == '__main__':
    cli()