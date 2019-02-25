
# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest

pytest_plugins = ['helpers_namespace',
                  'tests.fixtures.setup_failures',
                  'tests.fixtures.teardown_failures',
                  'tests.fixtures.test_list',
                  'tests.fixtures.xml_with_no_errors']


@pytest.fixture(scope='session')
def tempest_config_file(tmpdir_factory):

    filename = tmpdir_factory.mktemp('data').join('tempest_config.json').strpath

    config_json = \
        """{
              "tempest_zigzag_env_vars": {
                "BUILD_URL": null,
                "BUILD_NUMBER": null,
                "TEST_CYCLE": null,
                "PROJECT_ID": null
              },
              "zigzag": {
                "test_cycle": "{{ TEST_CYCLE }}",
                "project_id": "{{ PROJECT_ID }}",
                "module_hierarchy": [
                    "{{ strftime('%Y') }}",
                    "{{ strftime('%B') }}",
                    "{{ zz_testcase_class }}"
                ],
                "build_url": "{{ BUILD_URL }}",
                "build_number": "{{ BUILD_NUMBER }}"
              }
            }"""

    with open(filename, 'w') as f:
        f.write(config_json)

    return filename
