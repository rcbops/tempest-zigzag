from __future__ import absolute_import
import re
from lxml import etree


class TempestTestcaseList(object):

    _FULL_CLASSNAME = re.compile(r'^(\w|\.)*')
    _TEST_PARAMETERS = re.compile(r'\[(.*)\]')
    _TEMPEST_UUID_RGX = re.compile(r'(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)')

    def __init__(self, test_entry_string):
        """Creates a new Tempest Test Execution

        Args:
            test_entry_string: (str) A single line from 'tempest run --list-tests'
        """
        self._test_entry_string = test_entry_string
        self._xml_element = None
        self._time = '0.00'

    @property
    def xml_element(self):
        """Produces xml in the format produced by tempest
        property is a caching property

        Returns:
            etree.Element : an xml testcase element
        """

        if self._xml_element is None:
            # a dict key = name in xml, value = value if there is one
            d = {
                'name': self._xml_name,
                'classname': self.classname,
                'time': self.time
            }

            # build an etree element
            xml = etree.Element('testcase')
            for xml_attrib_name, value in list(d.items()):
                if value:  # only add attribute if there is a value for it
                    xml.attrib[xml_attrib_name] = value
            self._xml_element = xml

        return self._xml_element

    @property
    def _xml_name(self):
        """The name as it appears in the XML
        not to be confused with name which is the name of the test

        Returns:
            str: the value for name as it would appear in tempest xml
        """
        params = list(self.test_tags)
        params.insert(0, "id-{}".format(self.idempotent_id))
        params = ','.join(params)

        return "{name}[{params}]".format(name=self.name, params=params)

    @property
    def name(self):
        """The name

        Returns:
            str: The name of the test
            None
        """
        try:
            return self._FULL_CLASSNAME.match(self._test_entry_string).group(0).split('.')[-1]
        except AttributeError:
            return None

    @property
    def classname(self):
        """The classname

        Returns:
            str: The classname of the test
            None
        """

        try:
            return '.'.join(self._FULL_CLASSNAME.match(self._test_entry_string).group(0).split('.')[:-1])
        except AttributeError:
            return None

    @property
    def idempotent_id(self):
        """The idempotent ID

        Returns:
            str: The UUID of the test
            None
        """

        try:
            return self._TEMPEST_UUID_RGX.search(self._test_entry_string).group(0)
        except AttributeError:
            return None

    @property
    def time(self):
        """The elapsed time of the test case

        Returns:
            str: the time in string format
        """
        return self._time

    @time.setter
    def time(self, value):
        """Sets the time property

        Args:
            value: (str) the time in a string
        """
        self._time = value

    @property
    def test_tags(self):
        """The tags associated with this test

        Returns:
            list: A list of strings
            None
        """

        try:
            params = self._TEST_PARAMETERS.search(self._test_entry_string).group(1).split(',')
            return [param for param in params if self._TEMPEST_UUID_RGX.search(param) is None]
        except AttributeError:
            return None

    @property
    def xml_failure_elements(self):
        """The xml child elements with the tag failure
        """
        # TODO try and reraise
        return self.xml_element.findall('failure')

    @property
    def xml_error_elements(self):
        """The xml child elements with the tag error
        """
        # TODO try and reraise
        return self.xml_element.findall('error')

