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
@click.option('-o', '--output', "output", required=False, default=None, help="download output file")
@click.pass_context
def download(ctx, url, output):
    '''Downloading module'''
    LOGGER = ctx.obj
    LOGGER.INFO(f"Downloading {url} as {output}")
    subprocess.call(['wget', '-nc', f'{url}', '-O', f'{output}'])