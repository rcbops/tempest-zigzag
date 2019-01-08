from __future__ import absolute_import
import inspect
from lxml import etree


class TempestTestBase(object):

    def __init__(self):
        self._name = None
        self._classname = None
        self._idempotent_id = None
        self._test_tags = None
        self._time = None
        self._skips = None
        self._errors = None
        self._failures = None
        self._xml_element = None

    def combine(self, other):
        """Combines a second instance of this class with this instance of this class

        Args:
            other: (TempestTestBase)
        """

        def isprop(v):
            return isinstance(v, property)

        # TODO make more efficient???
        for propname in [name for (name, value) in inspect.getmembers(self, isprop)]:
            other_prop_value = getattr(other, propname)
            this_prop_value = getattr(self, propname)
            if this_prop_value is None:
                setattr(self, propname, other_prop_value)

    # ==================================================================================================================
    # XML related properties
    # ==================================================================================================================
    @property
    def xml_element(self):
        """Produces xml in the format produced by tempest"""

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
    def _failure_etrees(self):
        """A list of failure elements based on the failures property"""
        xml = etree.Element('failure')
        pass

    @property
    def _skipped_etrees(self):
        pass

    @property
    def _error_etree(self):
        pass

    @property
    def _xml_name(self):
        """The name as it appears in the XML
        not to be confused with name which is the name of the test
        """
        params = list(self.test_tags)
        params.insert(0, "id-{}".format(self.idempotent_id))
        params = ','.join(params)

        return "{name}[{params}]".format(name=self.name, params=params)

    # ==================================================================================================================
    # properties with setters and getters, getters should be re implemented on child classes
    # ==================================================================================================================

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def classname(self):
        return self._classname

    @classname.setter
    def classname(self, value):
        self._classname = value

    @property
    def idempotent_id(self):
        return self._idempotent_id

    @idempotent_id.setter
    def idempotent_id(self, value):
        self._idempotent_id = value

    @property
    def test_tags(self):
        return self._test_tags

    @test_tags.setter
    def test_tags(self, value):
        self._test_tags = value

    @property
    def time(self):
        return '0.00'

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def failures(self):
        return self._failures

    @failures.setter
    def failures(self, value):
        self._failures = value

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value

    @property
    def skips(self):
        return self._skips

    @skips.setter
    def skips(self, value):
        self._skips = value

