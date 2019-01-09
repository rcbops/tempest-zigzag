import pytest


@pytest.fixture(scope='session')
def file_test_list(tmpdir_factory, string_test_list):
    """An example of output from
    tempest run --list-tests
    """

    filename = tmpdir_factory.mktemp('data').join('file_test_list_one').strpath

    with open(filename, 'w') as f:
        f.write(string_test_list)

    return filename


@pytest.fixture(scope='session')
def string_test_list():
    """An example of output from
    tempest run --list-tests
    """

    junit_xml = \
        """
        tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_one[id-1fc6bdc8-0b6d-4cc7-9f30-9b04fabe5b90,smoke]
        tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_two[id-470e0b89-386f-407b-91fd-819737d0b335,negative]
        tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_three[id-6a326c69-654b-438a-80a3-34bcc454e138,smoke]
        tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_four[id-eabadde4-3cd7-4ec4-a4b5-5a936d2d4408,network]
        tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_five[id-dc9ffd51-1c50-4f0e-a820-ae6d2a568a9e]
        tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_one[id-96be03c7-570d-409c-90f8-e4db3c646996]
        tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_two[id-eeef473c-7c52-494d-9f09-2ed7fc8fc036]
        tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_three[id-7f6a1cc5-2446-4cdb-9baa-b6ae0a919b72]
        tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_four[id-c8e85064-e79b-4906-9931-c11c24294d02]
        tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_five[id-0d148aa3-d54c-4317-aa8d-42040a475e20,smoke,negative,volume]
        """

    return junit_xml
