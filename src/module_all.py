# from _typeshed import NoneType
import sys
import os
import click
from click.decorators import pass_context
from src.click_context import cli
from src.module_download import download_cli
from src.module_indexing import kmers_cli as index_kmers
from src.module_indexing import validate_kSize
from src.module_transform import transform_cli
from src.module_pairwise import pairwise_cli
from src.module_filtering import filtering_cli
from src.module_matches import match_cli
import urllib
import requests
import subprocess
import re
from glob import glob
from itertools import product


@click.pass_context
def auto(ctx, *args):
    # print(args)
    ref1_url, ref2_url, kSize, jaccard, containment, all_fasta_files = args
    LOGGER = ctx.obj

    all_fasta_files = '-'.join(all_fasta_files)

    _ref1_basename = os.path.basename(ref1_url).replace('.gz', '').strip()
    _ref2_basename = os.path.basename(ref2_url).replace('.gz', '').strip()
    _common_substr = list(set(_ref1_basename.split('.')).intersection(set(_ref2_basename.split('.'))))
    _common_substr.append(".")

    ref1_nickname = re.sub(r'|'.join(map(re.escape, _common_substr)), '', _ref1_basename).replace('.fa','').upper()
    ref2_nickname = re.sub(r'|'.join(map(re.escape, _common_substr)), '', _ref2_basename).replace('.fa','').upper()


    if _ref1_basename not in all_fasta_files:
        ctx.invoke(download_cli, url = ref1_url, output = _ref1_basename)

    if _ref2_basename not in all_fasta_files:
        ctx.invoke(download_cli, url = ref2_url, output = _ref2_basename)

    # Transform
    if ref1_nickname not in all_fasta_files:
        LOGGER.INFO(f"Transforming {_ref1_basename}")
        ctx.invoke(transform_cli, fasta_file = _ref1_basename, reference_nickname = ref1_nickname)
    
    if ref2_nickname not in all_fasta_files:
        LOGGER.INFO(f"Transforming {_ref2_basename}")
        ctx.invoke(transform_cli, fasta_file = _ref2_basename, reference_nickname = ref2_nickname)

    ## Merging files for indexing
    merged_file_name = f"merged_{ref1_nickname}_{ref2_nickname}"

    if f"{merged_file_name}.fa" not in all_fasta_files:
        LOGGER.INFO(f"Merging files for kProcessor index")
        cmd = f"""
            cat {ref1_nickname}.fa {ref2_nickname}.fa > {merged_file_name}.fa && cat {ref1_nickname}.fa.names {ref2_nickname}.fa.names > {merged_file_name}.fa.names   
        """
        subprocess.check_output(cmd, shell=True, executable='/bin/bash')


    # Indexing
    idx_prefix = f"idx_{merged_file_name}"
    if idx_prefix not in all_fasta_files:
        LOGGER.INFO(f"Indexing ...")
        ctx.invoke(index_kmers, fasta_file = f"{merged_file_name}.fa", names_file = f"{merged_file_name}.fa.names", kSize = kSize, chunkSize = 5000, canonical = False, output_prefix = idx_prefix)

    # Pairwise and annotating
    if f"{idx_prefix}_nodes_size.tsv" not in all_fasta_files:
        ctx.invoke(pairwise_cli, index_prefix = idx_prefix)
    
    # Filtering
    if f"{idx_prefix}_relations.csv" not in all_fasta_files:
        ctx.invoke(filtering_cli, index_prefix = idx_prefix, jaccard = jaccard, containment = containment)

    # Matching
    LOGGER.INFO(f"Matching {ref1_nickname} vs. {ref2_nickname}")
    if f"{ref1_nickname}_matches.tsv" not in all_fasta_files:
        ctx.invoke(match_cli, ref1_nickname = ref1_nickname, ref2_nickname = ref2_nickname, relations_file = f"{idx_prefix}_relations.csv")

    LOGGER.SUCCESS(f"Processing done for {ref1_nickname} vs. {ref2_nickname}")



@cli.command(name="auto", help_priority=1)
@click.option('--refs-tsv', "refs_tsv", required=True, type=click.Path(exists=True), help="FASTA file")
@click.option('-j', '--min-jac', 'jaccard', required=True, type=click.INT, help="minimum jaccard similarity %")
@click.option('-c', '--min-cont', 'containment', required=True, type=click.INT, help="minimum containment similarity %")
@click.option('-k', '--kmer-size', "kSize", callback=validate_kSize, required=True, type=click.IntRange(7, 31, clamp=False), help="kmer size")
@click.pass_context
def auto_cli(ctx, kSize, refs_tsv, jaccard, containment):
    '''Automate the whole pipeline'''

    all_files = glob('./*')
    
    with open(refs_tsv) as TSV:
        for line in TSV:
            ref1_url, ref2_url = tuple(line.split('\t'))
            ctx.obj.INFO(f"Processing {ref1_url} vs. {ref2_url}")
            auto(ref1_url, ref2_url, kSize, jaccard, containment, all_files)