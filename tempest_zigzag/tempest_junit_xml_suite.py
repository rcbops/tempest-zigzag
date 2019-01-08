from __future__ import absolute_import
from future.moves.collections import MutableSequence
from lxml import etree
from tempest_zigzag.tempest_testcase_xml import TempestTestcaseXml


class TempestJunitSuite(MutableSequence):
    """maps directly to an XML suite
    Can create an xml string
    """

    def __init__(self, path):
        """Create a new TempestJunitSuite

        Args:
            path: (str) the path to the file to be read
        """
        # read the xml
        junit_xml_doc = etree.parse(path)
        self._initial_junit_xml = junit_xml_doc.getroot()
        # read the testcases from the xml
        self._test_list = [TempestTestcaseXml(element) for element in self._initial_junit_xml.findall('testcase')]

    def remove_tests_without_idempotent_ids(self):
        """Removes any test cases that do not have the idempotent_id property

        Returns:
            a list of the test cases removed
        """
        new_list = []
        tests_to_return = []

        for test in self._test_list:
            if not test.idempotent_id:
                tests_to_return.append(test)
            else:
                new_list.append(test)

        self._test_list = new_list

        return tests_to_return

    def find_tests_by_classname(self, classname):
        """gets a list of tests that match a classname"""
        return [test for test in self._test_list if test.classname == classname]

    @property
    def _xml_error_count(self):
        """The total number of tests with errors

        Returns:
            int: the number of tests with errors in this sequence
        """
        return len([test for test in self._test_list if test.xml_error_elements])

    @property
    def _xml_failure_count(self):
        """The total number of tests with failures

        Returns:
            int: the number of tests with failures in this sequence
        """
        return len([test for test in self._test_list if test.xml_failure_elements])

    @property
    def _xml_total_time(self):
        """The total time of all the tests contained in this sequence

        Returns:
            float: the total execution time
        """
        return sum([float(test.time) for test in self._test_list])

    @property
    def _xml_total_test_count(self):
        """The total number of tests contained in this sequence

        Returns:
            int: the number of tests in this sequence
        """
        return len(self._test_list)

    @property
    def xml(self):
        """Generate the xml based on the contents of this sequence"""
        # a dict key = name in xml, value = value if there is one
        d = {
            'errors': self._xml_error_count,
            'failures': self._xml_failure_count,
            'name': 'xml suite create by tempest-zigzag',
            'tests': self._xml_total_test_count,
            'time': self._xml_total_time,
        }

        # build an etree element
        xml = etree.Element('testsuite')
        for xml_attrib_name, value in list(d.items()):
            if value is not None:  # only add attribute if there is a value for it
                xml.attrib[xml_attrib_name] = str(value)

        # read all elements from this sequence and add as child elements
        for test in self._test_list:
            xml.append(test.xml_element)

        return etree.tostring(xml)

    def __getitem__(self, key):
        """MutableSequence ABC override."""

        return self._test_list.__getitem__(key)

    def __setitem__(self, key, value):
        """MutableSequence ABC override."""

        return self._test_list.__setitem__(key, value)

    def insert(self, index, value):
        """MutableSequence ABC override."""

        return self._test_list.insert(index, value)

    def __delitem__(self, index):
        """MutableSequence ABC override."""

        return self._test_list.__delitem__(index)

    def __len__(self):
        """MutableSequence ABC override."""

        return len(self._test_list)


