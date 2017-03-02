from noselfs import LfsTestBase
import os


class TestUnitTestBaseClass(LfsTestBase):
    def test_get_file(self):
        datadir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'data/unit')
        filepath = self.get_file(datadir, 'test_file.txt')

        self.assertNotEquals(os.path.join(datadir, 'test_file.txt'), filepath)
        self.assertTrue(os.path.isfile(filepath))


class TestUnitTestBaseClassTeardown(LfsTestBase):
    def test_class_creates_removes_temp_folder(self):
        self.assertTrue(os.path.isdir(self.testdir))

    def tearDown(self):
        super(TestUnitTestBaseClassTeardown, self).tearDown()
        self.assertFalse(os.path.isdir(self.testdir))
