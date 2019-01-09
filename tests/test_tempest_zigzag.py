from tempest_zigzag.tempest_zigzag import TempestZigZag
from lxml import etree


class TestTempestZigZag(object):

    def test_nothing_to_do(self, file_test_xml_all_pass, file_test_list):
        """Tests that when there is nothing to do it will return a string
        that is functionally identical to the xml passed in"""

        result = TempestZigZag.process_xml(file_test_xml_all_pass, file_test_list)
        expected = etree.parse(file_test_xml_all_pass).getroot()
        observed = etree.XML(result)

        assert observed.tag == expected.tag
        assert observed.attrib['failures'] == expected.attrib['failures']
        assert observed.attrib['errors'] == expected.attrib['errors']
        assert observed.attrib['tests'] == expected.attrib['tests']
        assert observed.attrib['name'] == 'xml suite created by tempest-zigzag'
        assert len(observed) == len(expected)  # the actual number of child elements (testcase)

        for observed_case in observed:
            # test that the observed cases have the same names as the expected cases
            assert len([case for case in expected if case.attrib['name'] == observed_case.attrib['name']]) is 1

    def test_setupclass_failure(self, file_test_xml_setup_failure, file_test_list):
        """Tests that the correct testcase elements will be created
        when a setUpClass failure is found"""

        result = TempestZigZag.process_xml(file_test_xml_setup_failure, file_test_list)
        observed = etree.XML(result)
        new_case_count = 0

        assert len(observed) is 10
        assert '5' == observed.attrib['errors']
        assert '0' == observed.attrib['failures']
        for testcase in observed.findall('testcase'):
            if testcase.attrib['classname'] == 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON':
                error_tag = testcase.find('error')
                assert error_tag is not None
                assert 'An unexpected error prevented the server from fulfilling your request.' in error_tag.text
                assert not testcase.find('failure')  # there should not be any failures
                new_case_count += 1
        assert new_case_count is 5

    def test_teardownclass_failure(self, file_test_xml_teardown_failure, file_test_list):
        """Tests that the correct testcase elements will be altered
        when a teardown failure is found"""

        result = TempestZigZag.process_xml(file_test_xml_teardown_failure, file_test_list)
        observed = etree.XML(result)

        assert len(observed) is 10
        assert '5' == observed.attrib['errors']
        assert '0' == observed.attrib['failures']
        for testcase in observed.findall('testcase'):
            if testcase.attrib['classname'] == 'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON':
                error_tag = testcase.find('error')
                assert error_tag is not None
                assert 'An unexpected error prevented the server from fulfilling your request.' in error_tag.text
                assert not testcase.find('failure')  # there should not be any failures

    def test_teardownclass_multiple_failures(self, file_test_xml_teardown_multiple_failures, file_test_list):
        """Tests that the correct testcase elements will be altered
        when multiple teardown failures are found"""

        result = TempestZigZag.process_xml(file_test_xml_teardown_multiple_failures, file_test_list)
        observed = etree.XML(result)

        assert len(observed) is 10
        assert '10' == observed.attrib['errors']
        assert '0' == observed.attrib['failures']
        # all test cases should be set to error in this case
        for testcase in observed.findall('testcase'):
            error_tag = testcase.find('error')
            assert error_tag is not None
            assert 'An unexpected error prevented the server from fulfilling your request.' in error_tag.text
            assert not testcase.find('failure')  # there should not be any failures

    def test_setupclass_multiple_failures(self, file_test_xml_setup_multiple_failures, file_test_list):
        """Tests that the correct testcase elements will be altered
        when multiple teardown failures are found"""

        result = TempestZigZag.process_xml(file_test_xml_setup_multiple_failures, file_test_list)
        observed = etree.XML(result)

        assert len(observed) is 10
        assert '10' == observed.attrib['errors']
        assert '0' == observed.attrib['failures']
        # all test cases should be set to error in this case
        for testcase in observed.findall('testcase'):
            error_tag = testcase.find('error')
            assert error_tag is not None
            assert 'An unexpected error prevented the server from fulfilling your request.' in error_tag.text
            assert not testcase.find('failure')  # there should not be any failures

    def test_teardownclass_failure_tests_not_found(self, file_test_xml_teardown_class_not_in_list, file_test_list):
        """Tests when a tearDownClass failure exists in the provided xml
        but there are no corresponding tests in the test list
        """

        result = TempestZigZag.process_xml(file_test_xml_teardown_class_not_in_list, file_test_list)
        expected = etree.parse(file_test_xml_teardown_class_not_in_list).getroot()
        observed = etree.XML(result)

        assert observed.tag == expected.tag
        assert observed.attrib['failures'] == expected.attrib['failures']
        assert observed.attrib['errors'] == expected.attrib['errors']
        assert observed.attrib['tests'] == expected.attrib['tests']
        assert observed.attrib['name'] == 'xml suite created by tempest-zigzag'
        assert len(observed) == len(expected)
        # the broken testcase should be the last case in the list
        assert 'tearDownClass (tempest.oops.this.class.is.not.in.the.TestList)' == observed[-1].attrib['name']

    def test_setupclass_failure_tests_not_found(self, file_test_xml_setup_class_not_in_list, file_test_list):
        """Tests when a setUpClass failure exists in the provided xml
        but there are no corresponding tests in the test list
        """

        result = TempestZigZag.process_xml(file_test_xml_setup_class_not_in_list, file_test_list)
        expected = etree.parse(file_test_xml_setup_class_not_in_list).getroot()
        observed = etree.XML(result)

        assert observed.tag == expected.tag
        assert observed.attrib['failures'] == expected.attrib['failures']
        assert observed.attrib['errors'] == expected.attrib['errors']
        assert observed.attrib['tests'] == expected.attrib['tests']
        assert observed.attrib['name'] == 'xml suite created by tempest-zigzag'
        assert len(observed) == len(expected)
        # the broken testcase should be the last case in the list
        assert 'setUpClass (tempest.oops.this.class.is.not.in.the.TestList)' == observed[-1].attrib['name']

