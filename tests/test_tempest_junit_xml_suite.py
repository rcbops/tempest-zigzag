from tempest_zigzag.tempest_junit_xml_suite import TempestJunitXMLSuite
from tempest_zigzag.tempest_testcase_xml import TempestTestcaseXml
from lxml import etree


class TestTempestJunitXMLSuite(object):

    def test_nothing_to_remove(self, file_test_xml_skip_error_fail):

        tjxmls = TempestJunitXMLSuite(file_test_xml_skip_error_fail)
        removed = tjxmls.remove_tests_without_idempotent_ids()
        starting_len = len(tjxmls)

        assert 0 == len(removed)
        assert starting_len == len(tjxmls)

    def test_remove_without_id(self, file_test_xml_teardown_multiple_failures):

        tjxmls = TempestJunitXMLSuite(file_test_xml_teardown_multiple_failures)
        starting_len = len(tjxmls)
        removed = tjxmls.remove_tests_without_idempotent_ids()

        assert 2 == len(removed)
        assert starting_len == len(tjxmls) + len(removed)
        for test in removed:
            assert test.idempotent_id is None

    def test_find_tests_by_classname(self, file_test_xml_skip_error_fail):

        tjxmls = TempestJunitXMLSuite(file_test_xml_skip_error_fail)

        for test in tjxmls.find_tests_by_classname(tjxmls[0].classname):
            assert tjxmls[0].classname == test.classname

    def test_generate_xml_after_removing_test_with_no_id(self, file_test_xml_teardown_multiple_failures):

        tjxmls = TempestJunitXMLSuite(file_test_xml_teardown_multiple_failures)
        tjxmls.remove_tests_without_idempotent_ids()
        xml_string = tjxmls.xml

        for testcase in etree.XML(xml_string):
            #  ID should be inside of the tempest formatted xml in the name attribute
            assert TempestTestcaseXml._TEMPEST_UUID_RGX.search(testcase.attrib['name'])
