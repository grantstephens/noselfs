from noselfs import lfstest
import unittest
import os
import pkg_resources


def dummy():
    return


class TestNoseLFSDecorator(unittest.TestCase):

    def test_file_name(self):
        lfsf = lfstest('unit', 'test_file.txt')
        lfsf(dummy)
        file_name_relative = os.path.join('data', 'unit', 'test_file.txt')
        file_name = pkg_resources.resource_filename(
            __name__, file_name_relative
            )
        self.assertEqual(lfsf.file_name, file_name)

    def test_file_exists(self):
        lfsf = lfstest('unit', 'test_fake_file.txt')
        with self.assertRaises(IOError):
            lfsf(dummy)

    # def test_lfs_exception(self):
    #     lfsf = lfstest('unit', 'fake_pointer.txt')
