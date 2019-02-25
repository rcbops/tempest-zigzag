# -*- coding: utf-8 -*-

"""Test cases for the 'get_xsd' utility function for retrieving the XSD for the project."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from tempest_zigzag.tempest_zigzag import TempestZigZag
from zigzag.xml_parsing_facade import XmlParsingFacade
from lxml import etree


# ======================================================================================================================
# Tests
# ======================================================================================================================
def test_valid_xsd_generation(file_test_xml_setup_failure, file_test_list_with_whitespace, tempest_config_file, mocker):
    """Verify that 'get_xsd' returns an XSD stream that can be used to validate JUnitXML."""

    # Mock
    zz = mocker.MagicMock()
    xmlpf = XmlParsingFacade(zz)

    result = TempestZigZag.process_xml(file_test_xml_setup_failure,
                                       file_test_list_with_whitespace,
                                       tempest_config_file)
    xml_doc = etree.fromstring(result)

    # noinspection PyProtectedMember
    xmlschema = etree.XMLSchema(etree.parse(xmlpf._get_xsd()))

    # Test
    xmlschema.assertValid(xml_doc)