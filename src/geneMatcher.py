import sys
import click

from src.click_context import cli
from src.module_download import download_cli
from src.module_indexing import kmers_cli as index_kmers
from src.module_transform import transform_cli
from src.module_pairwise import pairwise_cli
from src.module_filtering import filtering_cli
from src.module_matches import match_cli




cli.add_command(index_kmers, name="index")
cli.add_command(download_cli, name="download")
cli.add_command(transform_cli, name="transform")
cli.add_command(pairwise_cli, name="pairwise")
cli.add_command(filtering_cli, name="filter")
cli.add_command(match_cli, name="match")




if __name__ == '__main__':
    cli()