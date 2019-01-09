from __future__ import absolute_import
import re
from lxml import etree
from tempest_zigzag.tempest_junit_xml_suite import TempestJunitXMLSuite
from tempest_zigzag.tempest_test_list import TempestTestList


class TempestZigZag(object):

    @classmethod
    def process_xml(cls, junit_input_file_path, test_list_path):
        """Process the files into an xml string

        Args:
            junit_input_file_path: (str) the path to the junit xml file to be processed
            test_list_path: (str) the path to the test-list file

        Returns:
            str: the processed xml string
        """
        xml_suite = TempestJunitXMLSuite(junit_input_file_path)
        test_list = TempestTestList(test_list_path)

        broken_entries = xml_suite.remove_tests_without_idempotent_ids()
        if broken_entries:
            for broken in broken_entries:

                if re.match(r'setupclass', broken.name, re.IGNORECASE):

                    tests_to_alter = test_list.find_tests_by_classname(broken.classname_in_wrong_place)

                    if tests_to_alter:
                        for test in tests_to_alter:
                            # attach child elements to appropriate test cases from the test list
                            for child in broken.child_elements:
                                dup_child = cls._duplicate_child_failure_elements(
                                    child, "setUpClass error: {}".format(broken.classname_in_wrong_place))
                                test.xml_element.append(dup_child)
                            test.time = broken.time
                            xml_suite.append(test)  # insert reconstructed test records into the suite
                    else:
                        xml_suite.append(broken)  # if we can't create a new record we should put the broken record back

                elif re.match(r'teardownclass', broken.name, re.IGNORECASE):

                    tests_to_alter = xml_suite.find_tests_by_classname(broken.classname_in_wrong_place)

                    if tests_to_alter:
                        # find elements in the xml that match the classname of the broken entry
                        for test in tests_to_alter:
                            for child in broken.child_elements:  # add new tags to existing test in xml suite
                                dup_child = cls._duplicate_child_failure_elements(
                                    child, "tearDownClass error: {}".format(broken.classname_in_wrong_place))
                                test.xml_element.append(dup_child)
                    else:
                        xml_suite.append(broken)  # if we can't alter any records we should put the broken record back

        return xml_suite.xml

    @classmethod
    def _duplicate_child_failure_elements(cls, element, message):
        """Re-writes the tags of a list of failure elements
        also writes a new message attribute

        Args:
            element: (list) etree.Element
            message: (str) the message to use

        Returns:
            list: the altered list of elements
        """

        xml = etree.Element(element.tag)
        xml.text = element.text
        xml.attrib['type'] = element.attrib['type']
        xml.attrib['message'] = message
        if xml.tag == 'failure':  # only operate on failure tags
            xml.tag = 'error'

        return xml
