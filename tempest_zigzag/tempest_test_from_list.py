from __future__ import absolute_import
import re
from tempest_zigzag.tempest_test_base import TempestTestBase


class TempestTestFromList(TempestTestBase):

    _FULL_CLASSNAME = re.compile(r'^(\w|\.)*')
    _TEST_PARAMETERS = re.compile(r'\[(.*)\]')
    _TEMPEST_UUID_RGX = re.compile(r'(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)')

    def __init__(self, test_entry_string):
        """Creates a new Tempest Test Execution

        Args:
            test_entry_string: (str) A single line from 'tempest run --list-tests'
        """
        super(TempestTestFromList, self).__init__()
        self._test_entry_string = test_entry_string

    @property
    def name(self):
        """The name

        Returns:
            str: The name of the test
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
        """

        try:
            return self._TEMPEST_UUID_RGX.search(self._test_entry_string).group(0)
        except AttributeError:
            return None

    @property
    def test_tags(self):
        """The tags associated with this test

        Returns:
            list: A list of strings
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

