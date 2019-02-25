from __future__ import absolute_import
import re
from lxml import etree
from datetime import datetime
from datetime import timedelta


class TempestTestcaseXml(object):
    """A class that reads xml generated by tempest
    This class is not responsible for writing new xml based on data
    This class only provides an interface to read xml generated by tempest
    """

    _TEMPEST_UUID_RGX = re.compile(r'(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)')
    _CLASSNAME = re.compile(r'\((.*)\)')
    _date_time_format = '%Y-%m-%dT%H:%M:%SZ'  # the highest degree of accuracy that qtest will accept (no micro seconds)

    def __init__(self, xml_element):
        self._date_time_now = datetime.utcnow()
        self._xml_element = xml_element

    @property
    def start_time(self):
        """Gets the start time

        Returns:
            str: the end date of this test execution
        """
        return self._date_time_now.strftime(self._date_time_format)

    @property
    def end_time(self):
        """Gets the end time

        Returns:
            str: the end date of this test execution
        """

        start = datetime.strptime(self.start_time, self._date_time_format)
        # if time is a fraction of a second round up to one second
        time = 1 if float(self.time) < 1 else self.time
        duration = timedelta(seconds=float(time))
        end = start + duration
        return end.strftime(self._date_time_format)

    @property
    def idempotent_id(self):
        """The unique uuid for this test"""
        try:
            return self._TEMPEST_UUID_RGX.search(self.name).group(0)
        except AttributeError:
            return None

    @property
    def classname(self):
        """The value of the 'classname' attribute
        Taken straight from the xml
        """

        try:
            return self._xml_element.attrib['classname']
        except KeyError as e:
            raise TempestXMLAccessError(e)

    @property
    def classname_in_wrong_place(self):
        """The classname that sometimes appears in the name attribute

        Returns:
            str: the classname extracted from a broken entry
        """

        try:
            return self._CLASSNAME.search(self.name).group(1)
        except AttributeError:
            raise TempestXMLAccessError("Classname not found in name: {}".format(self.name))

    @property
    def name(self):
        """The value of the 'name' attribute
        Taken straight from the xml

        Returns:
            str: the name value from the xml
        """

        try:
            return self._xml_element.attrib['name']
        except KeyError as e:
            raise TempestXMLAccessError(e)

    @property
    def time(self):
        """The value of the 'time' attribute
        Taken straight from the xml

        Returns:
            str: the time value from the xml
        """

        try:
            return self._xml_element.attrib['time']
        except KeyError as e:
            raise TempestXMLAccessError(e)

    @property
    def xml_failure_elements(self):
        """The xml child elements with the tag failure

        Returns:
            list : list of all the child failure elements
        """

        return self._xml_element.findall('failure')

    @property
    def xml_error_elements(self):
        """The xml child elements with the tag error

        Returns:
            list : list of all child error elements
        """

        return self._xml_element.findall('error')

    @property
    def child_elements(self):
        """The xml child elements

        Returns:
            list : a list of child etree.Element
        """
        return list(self._xml_element)

    @property
    def xml_element(self):
        """The XML element that was passed in on instantiation
        This is used when we go to reconstruct the finished xml
        called only when we determine its accurate

        Returns:
            etree.Element
        """
        properties = etree.Element('properties')
        properties.append(etree.Element('property', {'name': 'start_time', 'value': self.start_time}))
        properties.append(etree.Element('property', {'name': 'end_time', 'value': self.end_time}))
        if self.idempotent_id:
            properties.append(etree.Element('property', {'name': 'test_id', 'value': self.idempotent_id}))
        properties.append(etree.Element('property', {'name': 'test_step', 'value': 'false'}))
        self._xml_element.append(properties)
        return self._xml_element


class TempestXMLAccessError(Exception):
    """An Error used by TempestTestcaseXml"""

    def __init__(self, message):
        """An error to raise in the event we cant find something we need in the xml"""
        super(TempestXMLAccessError, self).__init__(message)
