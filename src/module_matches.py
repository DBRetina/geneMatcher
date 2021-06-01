# from _typeshed import NoneType
import sys
import os
import click
from src.click_context import cli
import urllib
import requests
import subprocess

def keepTheGreatest(current_list, new_gene):
        current_list = current_list.copy()
        newGeneName, newGeneJacard, newGeneCont = new_gene
        newGeneScore = newGeneJacard + newGeneCont
        maxScoreFound = float()
        if not len(current_list):
            return []

        for currentGene in current_list:
            currentGeneName, currentGeneJacard, currentGeneCont = currentGene
            currentGeneScore = currentGeneJacard + currentGeneCont
            maxScoreFound = max(currentGeneScore, maxScoreFound)
        
        if newGeneScore == maxScoreFound:
            current_list.append(new_gene)
        elif newGeneScore > maxScoreFound:
            current_list = [new_gene]
        
        return current_list


@cli.command(name="match", help_priority=6)
@click.option('-n', '--ref1_nickname', "ref1_nickname", required=False, default=None, help="reference_1 nickname")
@click.option('-n', '--ref2_nickname', "ref2_nickname", required=False, default=None, help="reference_2 nickname")
@click.option('-r', '--rel', "relations_file", required=True, type=click.Path(exists=True), help="kSpider relations TSV")
@click.pass_context
def match_cli(ctx, ref1_nickname, ref2_nickname, relations_file):
    '''Generate best mutual matches'''
    LOGGER = ctx.obj
    LOGGER.INFO(f"Processing ..")

    tr1_prefix = ref1_nickname
    tr2_prefix = sys.argv[2]
    file1 = ref2_nickname


    tr1_tr1 = dict()
    tr1_tr2 = dict()

    tr2_tr2 = dict()
    tr2_tr1 = dict()

    with open(file1) as READER:
        next(READER)
        for line in READER:
            line = line.split('|')
            jaccard, containment = float(line[4]), float(line[5])
            gene1, gene2 = line[1], line[6]
            gene1_full = (gene1, jaccard, containment)
            gene2_full = (gene2, jaccard, containment)


            # gene1 & gene2 belongs to tr1
            if tr1_prefix in gene1 and tr1_prefix in gene2:
                if gene1 not in tr1_tr1:
                    tr1_tr1[gene1] = [gene2_full]
                else:
                    tr1_tr1[gene1] = keepTheGreatest(tr1_tr1[gene1], gene2_full)
            
                if gene2 not in tr1_tr1:
                    tr1_tr1[gene2] = [gene1_full]
                else:
                    tr1_tr1[gene2] = keepTheGreatest(tr1_tr1[gene2], gene1_full)

                    
            
            # gene1 & gene2 belongs to tr2
            elif tr2_prefix in gene1 and tr2_prefix in gene2:
                if gene1 not in tr2_tr2:
                    tr2_tr2[gene1] = [gene2_full]
                else:
                    tr2_tr2[gene1] = keepTheGreatest(tr2_tr2[gene1], gene2_full)

                if gene2 not in tr2_tr2:
                    tr2_tr2[gene2] = [gene1_full]
                else:
                    tr2_tr2[gene2] = keepTheGreatest(tr2_tr2[gene2], gene1_full)
            
            # gene1, gene2 belongs to tr1,tr2
            elif tr2_prefix in gene1+gene2 and tr1_prefix in gene1+gene2:
                if tr1_prefix in gene1:
                    if gene1 not in tr1_tr2:
                        tr1_tr2[gene1] = [gene2_full]
                    else:
                        tr1_tr2[gene1] = keepTheGreatest(tr1_tr2[gene1], gene2_full)

                    if gene2 not in tr2_tr1:
                        tr2_tr1[gene2] = [gene1_full]
                    else:
                        tr2_tr1[gene2] = keepTheGreatest(tr2_tr1[gene2], gene1_full)
                    
                else:
                    if gene1 not in tr2_tr1:
                        tr2_tr1[gene1] = [gene2_full]
                    else:
                        tr2_tr1[gene1] = keepTheGreatest(tr2_tr1[gene1], gene2_full)

                    if gene2 not in tr1_tr2:
                        tr1_tr2[gene2] = [gene1_full]
                    else:
                        tr1_tr2[gene2] = keepTheGreatest(tr1_tr2[gene2], gene1_full)


    def getResults(tr_list, gene):
        if gene in list(tr_list):
            return tr_list[gene]
        else:
            return "-"


    _del = '\t'

    with open(f"{tr1_prefix}_matches.tsv", 'w') as R:
        R.write(f"{tr1_prefix}{_del}{tr1_prefix}_local{_del}{tr2_prefix}_across\n")
        for tr1_gene1, tr1_gene2 in tr1_tr1.items():
            R.write(f"{tr1_gene1}{_del}{tr1_gene2}{_del}{getResults(tr1_tr2, tr1_gene1)}\n")

    with open(f"{tr2_prefix}_matches.tsv", 'w') as R:
        R.write(f"{tr2_prefix}{_del}{tr2_prefix}_local{_del}{tr1_prefix}_across\n")
        for tr2_gene1, tr2_gene2 in tr2_tr2.items():
            R.write(f"{tr2_gene1}{_del}{tr2_gene2}{_del}{getResults(tr2_tr1, tr2_gene1)}\n")


    

    