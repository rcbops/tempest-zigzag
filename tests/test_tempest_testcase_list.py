from tempest_zigzag.tempest_testcase_list import TempestTestcaseList
from lxml.etree import _Element
from lxml import etree
import pytest


@pytest.fixture
def single_test_list_entry():
    """A single line from the output of
    tempest run --list-tests
    """
    return "tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]"  # noqa


class TestTempestTestcaseList(object):

    def test_calculated_properties(self, single_test_list_entry):

        ttcl = TempestTestcaseList(single_test_list_entry)

        assert ttcl.name == 'test_five'
        assert ttcl.classname == 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON'
        assert ttcl.test_tags == ['smoke', 'negative', 'volume']
        assert ttcl.idempotent_id == '0d148aa3-d54c-4317-aa8d-42040a475e20'

    def test_create_xml_element(self, single_test_list_entry):

        ttcl = TempestTestcaseList(single_test_list_entry)
        element = ttcl.xml_element

        assert type(element) is _Element
        assert 'testcase' == element.tag
        assert 'test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]' == element.attrib['name']
        assert 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON' == element.attrib['classname']
        assert '0.00' == element.attrib['time']  # default time

    def test_can_set_time(self, single_test_list_entry):
        """Test the only property that has a setter"""

        ttcl = TempestTestcaseList(single_test_list_entry)
        ttcl.time = '34.56'

        assert '34.56' == ttcl.time

    def test_can_set_a_child_xml_element(self, single_test_list_entry):

        ttcl = TempestTestcaseList(single_test_list_entry)
        element = ttcl.xml_element
        element.append(etree.Element('totes_magotes'))

        assert ttcl.xml_element[1].tag == 'totes_magotes'

    def test_find_errors(self, single_test_list_entry):

        ttcl = TempestTestcaseList(single_test_list_entry)
        element = ttcl.xml_element
        element.append(etree.Element('error'))

        assert 1 == len(ttcl.xml_error_elements)

    def test_find_failures(self, single_test_list_entry):

        ttcl = TempestTestcaseList(single_test_list_entry)
        element = ttcl.xml_element
        element.append(etree.Element('failure'))

        assert 1 == len(ttcl.xml_failure_elements)

    def test_find_errors_not_present(self, single_test_list_entry):
        """Test that we can ask for error elements when there are none"""

        ttcl = TempestTestcaseList(single_test_list_entry)

        assert [] == ttcl.xml_error_elements

    def test_find_failures_not_present(self, single_test_list_entry):
        """Test that we can ask fot failure elements when there are none"""

        ttcl = TempestTestcaseList(single_test_list_entry)

        assert [] == ttcl.xml_failure_elements
