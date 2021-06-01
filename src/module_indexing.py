# from _typeshed import NoneType
import sys
import os
import click
from src.click_context import cli

try:
    import kProcessor as kp
except ImportError:
    click.secho("kProcessor package could not found.", fg="red", bold=True , file = sys.stderr) 

class Index:

    def __init__(self,logger_obj, fasta_file, names_file):
        self.Logger = logger_obj
        self.fasta_file = fasta_file
        self.names_file = names_file
        self.KF = None
        self.cKF = None

    def validate_names(self):
        '''validate names file for indexing'''

        self.Logger.INFO("validating names file..")

        with open(self.names_file) as names:
            for i, line in enumerate(names, 1):
                if len(line.strip().split("\t")) != 2:
                    self.Logger.ERROR(f"invalid names line detected at L{i}: '{line.strip()}'")

    def index(self, chunkSize, kSize, canonical = False):
        """
        peform indexing with given kSize
        """

        self.Logger.INFO(f"Indexing by Kmers with kSize: {kSize}, chunkSize: {chunkSize}")

        try:
            strandType_Hasher = kp.nonCanonicalInteger_Hasher

            if canonical:
                strandType_Hasher = kp.integer_hasher

            self.KF = kp.kDataFramePHMAP(kp.KMERS, strandType_Hasher, {"kSize":kSize})
            self.cKF = kp.index(self.KF, self.fasta_file, chunkSize, self.names_file)
            
            self.Logger.SUCCESS("Indexing Completed")

        except Exception as e:
            print(e)
            self.Logger.ERROR("Indexing failed")

    def write_to_disk(self, output_prefix):
        """save index file to disk"""

        try:
            self.cKF.save(output_prefix)
        except:
            self.Logger.ERROR("saving index to disk failed")


def validate_kSize(ctx, param, value):
    if not value % 2:
        raise click.BadParameter(f"kmer size: {value} is even, please enter an odd value.")
    return value



@cli.command(name="index", help_priority=1)
@click.option('-f', '--fasta', "fasta_file", required=True, type=click.Path(exists=True), help="FASTA file")
@click.option('-n', '--names', "names_file", required=True, type=click.Path(exists=True), help="Names file")
@click.option('-k', '--kmer-size', "kSize", callback=validate_kSize, required=True, type=click.IntRange(7, 31, clamp=False), help="kmer size")
@click.option('-c', '--chunk-size', 'chunkSize', required = False, default = 5000, type=click.INT, help = "chunk size")
@click.option('--canonical', is_flag=True, help = "strand non-specific")
@click.option('-o', '--output', "output_prefix", required=False, default=None, help="index output file prefix")
@click.pass_context
def kmers(ctx, fasta_file, names_file, kSize, chunkSize, canonical, output_prefix):
    '''FASTA file indexing by Kmers'''

    if not output_prefix:
        output_prefix = os.path.basename(fasta_file)
        output_prefix = "idx" + "_" + output_prefix

    idx = Index(logger_obj=ctx.obj, fasta_file=fasta_file, names_file=names_file)
    idx.validate_names()
    idx.index(chunkSize, kSize, canonical)
    idx.write_to_disk(output_prefix)