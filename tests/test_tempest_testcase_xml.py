from lxml import etree
from tempest_zigzag.tempest_testcase_xml import TempestTestcaseXml
import pytest
from lxml.etree import _Element


@pytest.fixture()
def teardown_failure(string_test_xml_teardown_failure):
    """An example of a teardown failure xml element"""

    return etree.XML(string_test_xml_teardown_failure)[7]


@pytest.fixture()
def setup_failure(string_test_xml_setup_failure):
    """An example of a setup failure xml element"""

    return etree.XML(string_test_xml_setup_failure)[5]


class TestTempestTestcaseXMLTeardownFailure(object):

    def test_properties(self, teardown_failure):

        ttcxml = TempestTestcaseXml(teardown_failure)

        assert 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON' == ttcxml.classname_in_wrong_place
        assert not ttcxml.classname  # classname should be in the wrong place ^
        assert 'tearDownClass (tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON)' == ttcxml.name
        assert '0.000' == ttcxml.time
        assert ttcxml.idempotent_id is None

    def test_xml_elements(self, teardown_failure):

        ttcxml = TempestTestcaseXml(teardown_failure)
        element = ttcxml.xml_element

        assert type(element) is _Element  # this is the original element
        assert type(ttcxml.xml_failure_elements) is list
        assert 'failure' == ttcxml.xml_failure_elements[0].tag


class TestTempestTestcaseXMLSetupFailure(object):

    def test_properties(self, setup_failure):

        ttcxml = TempestTestcaseXml(setup_failure)

        assert 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON' == ttcxml.classname_in_wrong_place
        assert not ttcxml.classname  # classname should be in the wrong place ^
        assert 'setUpClass (tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON)' == ttcxml.name
        assert '0.000' == ttcxml.time
        assert ttcxml.idempotent_id is None

    def test_xml_elements(self, setup_failure):

        ttcxml = TempestTestcaseXml(setup_failure)
        element = ttcxml.xml_element

        assert type(element) is _Element  # this is the original element
        assert type(ttcxml.xml_failure_elements) is list
        assert 'failure' == ttcxml.xml_failure_elements[0].tag
