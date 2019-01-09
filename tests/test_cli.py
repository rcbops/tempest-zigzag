# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from tempest_zigzag import cli
from click.testing import CliRunner
from lxml import etree


def test_cli_happy_path(file_test_xml_all_pass, file_test_list):
    """Tests that the CLI will exit 0 and print out parsable xml when there is nothing to do"""

    runner = CliRunner()
    cli_arguments = [file_test_xml_all_pass, file_test_list]

    result = runner.invoke(cli.main, args=cli_arguments)
    assert 0 == result.exit_code
    assert etree.XML(result.output) is not None


def test_cli_mix_up_args(file_test_xml_all_pass, file_test_list):
    """Tests that tempest-zigzag will exit non-zero if args are transposed"""

    runner = CliRunner()
    cli_arguments = [file_test_list, file_test_xml_all_pass]

    result = runner.invoke(cli.main, args=cli_arguments)
    assert result.exit_code is not 0
