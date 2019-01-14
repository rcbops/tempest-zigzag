from tempest_zigzag.tempest_test_list import TempestTestList
from tempest_zigzag.tempest_testcase_list import TempestTestcaseList


class TestTempestTestList(object):

    def test_find_by_classname(self, file_test_list):

        tl = TempestTestList(file_test_list)
        for test in tl.find_tests_by_classname(tl[0].classname):
            assert type(test) is TempestTestcaseList
            assert tl[0].classname == test.classname
