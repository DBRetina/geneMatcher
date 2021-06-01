# from _typeshed import NoneType
import sys
import os
import click
from src.click_context import cli
import urllib
import requests
import subprocess


@cli.command(name="pairwise", help_priority=4)
@click.option('-i', '--index-prefix', 'index_prefix', required=True, type=click.STRING, help="kProcessor index file prefix")
@click.pass_context
def pairwise_cli(ctx, index_prefix):
    '''Generate pairwise similarity matrix'''
    LOGGER = ctx.obj
    LOGGER.INFO(f"Generating pairwise similarity matrix\nPlease wait ...")
    subprocess.call(['kSpider2', 'pairwise', '-i', index_prefix])

    LOGGER.INFO(f"Annotating the results ...")
    cmd = f"""
    paste <(tail -n+2 {index_prefix}.namesMap | cut -d" " -f1)  <(tail -n+2 {index_prefix}.namesMap |cut -d" " -f2-) > {index_prefix}.namesMap.tmp
    """

    subprocess.check_output(cmd, shell=True, executable='/bin/bash')

    cmd = f"""
    echo "node_id node_name size" | tr ' ' '\t' > {index_prefix}_nodes_size.tsv
    """
    subprocess.check_output(cmd, shell=True, executable='/bin/bash')

    cmd = f"""
    awk 'BEGIN{{FS=OFS="\t";}}FNR==NR{{a[$2]=$3;next;}}{{if(a[$1]!="")print $0,a[$1]}}' {index_prefix}_kSpider_seqToKmersNo.tsv {index_prefix}.namesMap.tmp >> {index_prefix}_nodes_size.tsv
    """
    subprocess.check_output(cmd, shell=True, executable='/bin/bash')

    cmd = f"""
    rm {index_prefix}.namesMap.tmp*
    """
    subprocess.check_output(cmd, shell=True, executable='/bin/bash')
