# -*- coding: utf-8 -*-

"""Console script for tempest-zigzag."""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import click
from tempest_zigzag.tempest_zigzag import TempestZigZag


# ======================================================================================================================
# Main
# ======================================================================================================================
@click.command()
@click.argument('junit_input_file', type=click.Path(exists=True))
@click.argument('test_list', type=click.Path(exists=True))
def main(junit_input_file, test_list):
    """Process multiple files created by tempest into a single accurate junit xml artifact"""
    TempestZigZag(junit_input_file, test_list)


if __name__ == "__main__":
    main()  # pragma: no cover
