# from _typeshed import NoneType
import sys
import os
import click
from src.click_context import cli
import urllib
import requests
import subprocess

def open_url(ctx, param, value):
    if value is not None:
        ctx.params['fp'] = urllib.urlopen(value)
        return value

@cli.command(name="transform", help_priority=2)
@click.option('-f', '--fasta', "fasta_file", required=True, type=click.Path(exists=True), help="FASTA file")
@click.option('-n', '--nickname', "reference_nickname", required=False, default=None, help="reference nickname")
@click.pass_context
def transform_cli(ctx, fasta_file, reference_nickname):
    '''Transform downloaded files'''
    LOGGER = ctx.obj

    if not reference_nickname:
        reference_nickname = "transformed_" + os.path.basename(fasta_file).replace(".fa",'')
    else:
        if ".fa" in reference_nickname:
            reference_nickname = reference_nickname.replace(".fa", '')

    LOGGER.INFO(f"Transforming {fasta_file} to {reference_nickname}")
    LOGGER.INFO(f"Generating names file {reference_nickname}.fa.names")

    with open(f"{reference_nickname}.fa.names", 'w') as NAMES_FILE, open(fasta_file) as FASTA, open(f"{reference_nickname}.fa", 'w') as TRANSFORMED_FASTA:
        for line in FASTA:
            if line.startswith('>'):
                line = line.replace('>', f">{reference_nickname}|")
                TRANSFORMED_FASTA.write(line)
                splitted = line[1:-1].split('|')
                groupName = f"{splitted[0]}_{splitted[2]}"
                NAMES_FILE.write(f"{line[1:-1]}\t{groupName}\n")
            else:
                TRANSFORMED_FASTA.write(line)
