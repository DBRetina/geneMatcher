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

@cli.command(name="download", help_priority=2)
@click.option('-u', '--url', "url", required=True, help="URL")
@click.option('-o', '--output', "output", required=False, default=None, help="download output file (omit gz to uncompress)")
@click.pass_context
def download(ctx, url, output):
    '''Downloading module'''
    LOGGER = ctx.obj

    compressed = False

    if not len(output):
        output = os.path.basename(url)
        compressed = True
    else:
        if "gz" in output:
            # compressed
            compressed = True
        else:
            # uncompressed
            compressed = False

    if compressed:
        LOGGER.INFO(f"Downloading {url} as {output}")
        subprocess.call(['wget', '-nc', f'{url}', '-O', f'{output}'])

    if not compressed:
        LOGGER.INFO(f"Downloading & Extracting {url} as {output}")
        subprocess.call(['wget', '-nc', f'{url}', '-O', f'{output}.gz'])
        f = open(output, "w")
        LOGGER.INFO(f"Extracting {output}")
        subprocess.call(["gunzip", "-c", f'{output}.gz'], stdout=f)
        f.close()
        LOGGER.INFO(f"Deleting the copmpressed file")
        subprocess.call(["rm", "-rf", f'{output}.gz'])
    