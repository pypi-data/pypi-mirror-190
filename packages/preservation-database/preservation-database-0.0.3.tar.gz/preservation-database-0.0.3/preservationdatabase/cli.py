import csv
import re
import sys
import inspect
import os.path

import click
import requests
from io import StringIO
from csv import DictReader

import logging

from rich.logging import RichHandler
from rich.console import Console

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True))]
)
log = logging.getLogger("rich")

sys.path.append(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django

django.setup()

from preservationdatabase.models import CarinianaPreservation, \
    ClockssPreservation, HathiPreservation, LockssPreservation, \
    PKPPreservation, PorticoPreservation, Publisher
from django.db import transaction
import utils


@click.group()
def cli():
    pass


@click.command()
@click.option('--url',
              default='https://api.portico.org/kbart/Portico_Holding_KBart.txt',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_portico(url, local):
    """Download and import data from Portico"""
    PorticoPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_clockss(url, local):
    """Download and import data from CLOCKSS"""
    ClockssPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_lockss(url, local):
    """Download and import data from LOCKSS"""
    LockssPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://pkp.sfu.ca/files/pkppn/onix.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_pkp(url, local):
    """Download and import data from PKP's private LOCKSS network"""
    PKPPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_cariniana(url, local):
    """Download and import data from Cariniana"""
    CarinianaPreservation.import_data(url, local=local)


def unpack_range(s):
    """ Converts a range of numbers to a full set"""
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l, h = map(int, i.split('-'))
            r += range(l, h + 1)
    return r


@click.command()
@click.option('--file',
              default='/home/martin/Downloads/hathi_full_20230101.txt',
              help='The Hathitrust full dump to use')
@transaction.atomic()
def import_hathi(file):
    """Import data from Hathi (requires local file download)"""
    log.info('[green]Opening:[/] Hathi data', extra={'markup': True})
    # clear out
    log.info('[green]Clearing:[/] previous Hathi data',
             extra={'markup': True})
    HathiPreservation.objects.all().delete()

    csv.field_size_limit(sys.maxsize)

    with open(file) as input_file:
        csv_reader = csv.reader(input_file, delimiter='\t')

        volume_matcher = r'v\.\s?(\d+(?:\-?\d+)?)'
        no_matcher = r'no\.\s?(\d+(?:\-?\d+)?)'
        year_matcher = r'\d{4}'

        for row in csv_reader:
            try:
                vols = row[4]
                issn = row[9]
                title = row[11]
                publishing_info = row[12]
                date = row[16]
                bf = row[19]
                unknown_format = False

                # if it's a serial, try to parse the vols
                if bf == 'SE' and issn and vols:
                    matches = re.findall(volume_matcher, vols)

                    if matches:
                        for match in matches:
                            vols = unpack_range(match)
                    else:
                        matches = re.findall(no_matcher, vols)

                        if matches:
                            for match in matches:
                                vols = unpack_range(match)
                        else:

                            matches = re.findall(year_matcher, vols)

                            if matches:
                                for match in matches:
                                    vols = match
                            else:
                                unknown_format = True

                    if not unknown_format:
                        if title.endswith('.'):
                            title = title[:-1]

                        HathiPreservation.objects.create(
                            issn=issn,
                            title=title,
                            preserved_volumes=vols
                        )

                        log.info('[green]Added:[/] {} to Hathi'.format(title),
                                 extra={'markup': True})
            except IndexError:
                pass


@click.command()
def import_all():
    """Download and import all data (excluding HathiTrust)"""

    import_clockss(
        url='https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv'
    )

    import_portico(
        url='https://api.portico.org/kbart/Portico_Holding_KBart.txt'
    )

    import_lockss(
        url='https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv'
    )

    import_cariniana(
        url='http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv'
    )


@click.command()
@click.option('--doi',
              help='The DOI to lookup for preservation status')
def show_preservation(doi):
    """
    Determine whether a DOI is preserved
    """
    doi = utils.normalize_doi(doi)
    preservation_statuses, doi = utils.show_preservation_for_doi(doi)

    for key, value in preservation_statuses.items():
        preserved, done = value

        if preserved:
            if done:
                log.info(f'[green]Preserved:[/] in {key}',
                         extra={'markup': True})
            else:
                log.info(f'[yellow]Preserved (in progress):[/] '
                         f'in {key}',
                         extra={'markup': True})
        else:
            log.info(f'[red]Not preserved:[/] in {key}',
                     extra={'markup': True})


if __name__ == '__main__':
    cli.add_command(import_all)
    cli.add_command(import_cariniana)
    cli.add_command(import_clockss)
    cli.add_command(import_hathi)
    cli.add_command(import_lockss)
    cli.add_command(import_pkp)
    cli.add_command(import_portico)
    cli.add_command(show_preservation)
    cli()
