import pytest


# ======================================================================================================================
# File fixtures
# ======================================================================================================================

@pytest.fixture(scope='session')
def file_test_xml_teardown_failure(tmpdir_factory, string_test_xml_teardown_failure):

    filename = tmpdir_factory.mktemp('data').join('string_test_xml_teardown_failure.xml').strpath

    with open(filename, 'w') as f:
        f.write(string_test_xml_teardown_failure)

    return filename


@pytest.fixture(scope='session')
def file_test_xml_teardown_multiple_failures(tmpdir_factory, string_test_xml_teardown_multiple_failures):

    filename = tmpdir_factory.mktemp('data').join('string_test_xml_teardown_failure.xml').strpath

    with open(filename, 'w') as f:
        f.write(string_test_xml_teardown_multiple_failures)

    return filename


@pytest.fixture(scope='session')
def file_test_xml_teardown_class_not_in_list(tmpdir_factory, string_test_xml_teardown_class_not_in_list):

    filename = tmpdir_factory.mktemp('data').join('string_test_xml_teardown_failure.xml').strpath

    with open(filename, 'w') as f:
        f.write(string_test_xml_teardown_class_not_in_list)

    return filename


# ======================================================================================================================
# String fixtures
# ======================================================================================================================

@pytest.fixture(scope='session')
def string_test_xml_teardown_failure():
    """This fixture represents a failure in a teardown class"""

    junit_xml = \
        """
        <testsuite errors="0" failures="1" name="" tests="11" time="1956.921">
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_one[id-1fc6bdc8-0b6d-4cc7-9f30-9b04fabe5b90,smoke]" time="18.794"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_two[id-470e0b89-386f-407b-91fd-819737d0b335,negative]" time="8.765"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_three[id-6a326c69-654b-438a-80a3-34bcc454e138,smoke]" time="9.039"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_four[id-eabadde4-3cd7-4ec4-a4b5-5a936d2d4408,network]" time="0.210"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_five[id-dc9ffd51-1c50-4f0e-a820-ae6d2a568a9e]" time="0.115"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_one[id-96be03c7-570d-409c-90f8-e4db3c646996]" time="0.120"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_two[id-eeef473c-7c52-494d-9f09-2ed7fc8fc036]" time="0.373"/>
            <testcase classname="" name="tearDownClass (tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON)" time="0.000">
              <failure type="testtools.testresult.real._StringException">Traceback (most recent call last):
              testtools.testresult.real._StringException: Traceback (most recent call last):
                File "/openstack/venvs/tempest-r14.20.0/tempest/lib/common/rest_client.py", line 829, in _error_checker
                  message=message)
              tempest.lib.exceptions.ServerFault: Got server fault
              Details: An unexpected error prevented the server from fulfilling your request.
            
              </failure>
            </testcase>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_three[id-7f6a1cc5-2446-4cdb-9baa-b6ae0a919b72]" time="0.141"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_four[id-c8e85064-e79b-4906-9931-c11c24294d02]" time="0.121"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]" time="0.115"/>
        </testsuite>
        """

    return junit_xml


@pytest.fixture(scope='session')
def string_test_xml_teardown_multiple_failures():
    """This fixture represents two separate failures
    in two different teardown classes"""

    junit_xml = \
        """
        <testsuite errors="0" failures="1" name="" tests="11" time="1956.921">
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_one[id-1fc6bdc8-0b6d-4cc7-9f30-9b04fabe5b90,smoke]" time="18.794"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_two[id-470e0b89-386f-407b-91fd-819737d0b335,negative]" time="8.765"/>
            <testcase classname="" name="tearDownClass (tempest.api.compute.admin.test_agents.AgentsAdminTestJSON)" time="0.000">
              <failure type="testtools.testresult.real._StringException">Traceback (most recent call last):
              testtools.testresult.real._StringException: Traceback (most recent call last):
                File "/openstack/venvs/tempest-r14.20.0/tempest/lib/common/rest_client.py", line 829, in _error_checker
                  message=message)
              tempest.lib.exceptions.ServerFault: Got server fault
              Details: An unexpected error prevented the server from fulfilling your request.
            
              </failure>
            </testcase>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_three[id-6a326c69-654b-438a-80a3-34bcc454e138,smoke]" time="9.039"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_four[id-eabadde4-3cd7-4ec4-a4b5-5a936d2d4408,network]" time="0.210"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_five[id-dc9ffd51-1c50-4f0e-a820-ae6d2a568a9e]" time="0.115"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_one[id-96be03c7-570d-409c-90f8-e4db3c646996]" time="0.120"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_two[id-eeef473c-7c52-494d-9f09-2ed7fc8fc036]" time="0.373"/>
            <testcase classname="" name="tearDownClass (tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON)" time="0.000">
              <failure type="testtools.testresult.real._StringException">Traceback (most recent call last):
              testtools.testresult.real._StringException: Traceback (most recent call last):
                File "/openstack/venvs/tempest-r14.20.0/tempest/lib/common/rest_client.py", line 829, in _error_checker
                  message=message)
              tempest.lib.exceptions.ServerFault: Got server fault
              Details: An unexpected error prevented the server from fulfilling your request.
            
              </failure>
            </testcase>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_three[id-7f6a1cc5-2446-4cdb-9baa-b6ae0a919b72]" time="0.141"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_four[id-c8e85064-e79b-4906-9931-c11c24294d02]" time="0.121"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]" time="0.115"/>
        </testsuite>
        """

    return junit_xml


@pytest.fixture(scope='session')
def string_test_xml_teardown_class_not_in_list():
    """An example containing 10 passes"""

    junit_xml = \
        """
        <testsuite errors="0" failures="1" name="" tests="11" time="1956.921">
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_one[id-1fc6bdc8-0b6d-4cc7-9f30-9b04fabe5b90,smoke]" time="18.794"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_two[id-470e0b89-386f-407b-91fd-819737d0b335,negative]" time="8.765"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_three[id-6a326c69-654b-438a-80a3-34bcc454e138,smoke]" time="9.039"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_four[id-eabadde4-3cd7-4ec4-a4b5-5a936d2d4408,network]" time="0.210"/>
            <testcase classname="tempest.api.compute.admin.test_agents.AgentsAdminTestJSON" name="test_five[id-dc9ffd51-1c50-4f0e-a820-ae6d2a568a9e]" time="0.115"/>
            <testcase classname="" name="tearDownClass (tempest.oops.this.class.is.not.in.the.TestList)" time="0.000">
              <failure type="testtools.testresult.real._StringException">Traceback (most recent call last):
              testtools.testresult.real._StringException: Traceback (most recent call last):
                File "/openstack/venvs/tempest-r14.20.0/tempest/lib/common/rest_client.py", line 829, in _error_checker
                  message=message)
              tempest.lib.exceptions.ServerFault: Got server fault
              Details: An unexpected error prevented the server from fulfilling your request.
            
              </failure>
            </testcase>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_one[id-96be03c7-570d-409c-90f8-e4db3c646996]" time="0.120"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_two[id-eeef473c-7c52-494d-9f09-2ed7fc8fc036]" time="0.373"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_three[id-7f6a1cc5-2446-4cdb-9baa-b6ae0a919b72]" time="0.141"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_four[id-c8e85064-e79b-4906-9931-c11c24294d02]" time="0.121"/>
            <testcase classname="tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON" name="test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]" time="0.115"/>
        </testsuite>
        """

    return junit_xml
