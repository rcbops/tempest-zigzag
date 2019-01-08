from __future__ import absolute_import
import re
from lxml import etree
from tempest_zigzag.tempest_junit_xml_suite import TempestJunitSuite
from tempest_zigzag.tempest_test_list import TempestTestList


class TempestZigZag(object):

    def __init__(self, junit_input_file, test_list):
        xml_suite = TempestJunitSuite(junit_input_file)
        test_list = TempestTestList(test_list)

        broken_entries = xml_suite.remove_tests_without_idempotent_ids()
        if broken_entries:
            for broken in broken_entries:
                # look up all tests that share the class name
                # TODO alter behavior so that if it cant find a matching test it puts the broken record back in

                if re.match(r'setupclass', broken.name, re.IGNORECASE):

                    tests_to_alter = test_list.find_tests_by_classname(broken.classname_in_wrong_place)

                    if tests_to_alter:
                        for test in tests_to_alter:
                            # attach child elements to appropriate test cases from the test list
                            for child in broken.child_elements:
                                dup_child = self._duplicate_child_failure_elements(child, "setUpClass error: {}".format(broken.classname_in_wrong_place))
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
                                dup_child = self._duplicate_child_failure_elements(child, "tearDownClass error: {}".format(broken.classname_in_wrong_place))
                                test.xml_element.append(dup_child)
                    else:
                        xml_suite.append(broken)  # if we can't alter any records we should put the broken record back

            with open(junit_input_file, 'w') as f:
                f.write(xml_suite.xml)  # overwrite if there are changes to make

    @staticmethod
    def _duplicate_child_failure_elements(element, message):
        """Re-writes the tags of a list of failure elements
        also writes a new message attribute

        Args:
            elements: (list) etree.Element
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
