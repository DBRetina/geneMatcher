# from _typeshed import NoneType
import sys
import os
import click
from src.click_context import cli
import urllib
import requests
import subprocess


@cli.command(name="filter", help_priority=5)
@click.option('-i', '--index-prefix', 'index_prefix', required=True, type=click.STRING, help="kProcessor index file prefix")
@click.option('-j', '--min-jac', 'jaccard', required=True, type=click.INT, help="minimum jaccard similarity %")
@click.option('-c', '--min-cont', 'containment', required=True, type=click.INT, help="minimum containment similarity %")
@click.pass_context
def filtering_cli(ctx, index_prefix, jaccard, containment):
    '''Filtering with jaccard and containment'''
    LOGGER = ctx.obj
    LOGGER.INFO(f"Filtering the results with min jaccard = {jaccard}, min containment = {containment} ...")

    cmd = f"""
    echo ":START_ID|START_name|START_size|shared_count:int|jDist:float|smPerc:float|END_name|END_size|:END_ID" > {index_prefix}_relations.csv
    """
    subprocess.check_output(cmd, shell=True, executable='/bin/bash')

    cmd = f"""
    awk -v md={jaccard} -v mc={containment} 'BEGIN{{FS="\t";S="|";}}FNR==NR{{a[$1]=$3;b[$1]=$2S$3;next;}}{{
   g1=a[$2]; g2=a[$3]; min=g1;min=(min < g2 ? min : g2); 
   jDist=$4*100/(g1+g2-$4); smPerc=$4*100/min; 
   if(jDist>md || smPerc>mc)
     printf("%s%s%s%s%s%s%.1f%s%.1f%s%s%s%s\\n", $2,S,b[$2],S,$4,S,jDist,S,smPerc,S,b[$3],S,$3)}}' \
   {index_prefix}_nodes_size.tsv <(tail -n+2 {index_prefix}_kSpider_pairwise.tsv) >> {index_prefix}_relations.csv
    """

    subprocess.check_output(cmd, shell=True, executable='/bin/bash')


    

    