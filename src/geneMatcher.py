import sys
import click

from src.click_context import cli
from src.module_indexing import kmers as index_kmers
from src.module_download import download
from src.module_transform import transform
from src.module_pairwise import pairwise



cli.add_command(index_kmers, name="index")
cli.add_command(download, name="download")
cli.add_command(transform, name="transform")
cli.add_command(pairwise, name="pairwise")



if __name__ == '__main__':
    cli()