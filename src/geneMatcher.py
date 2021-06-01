import sys
import click

from src.click_context import cli
from src.module_indexing import kmers as index_kmers
from src.module_download import download



cli.add_command(index_kmers, name="index")
cli.add_command(download, name="download")


if __name__ == '__main__':
    cli()