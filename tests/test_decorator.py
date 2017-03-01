from noselfs import lfstest
import unittest
import os
import pkg_resources


def dummy():
    return


class TestNoseLFSDecorator(unittest.TestCase):

    def test_file_name(self):
        lfsf = lfstest('test_file.txt', 'data', 'unit')
        lfsf(dummy)
        file_name_relative = os.path.join('data', 'unit', 'test_file.txt')
        file_name = pkg_resources.resource_filename(
            __name__, file_name_relative
            )
        self.assertEqual(lfsf.file_name, file_name)

    def test_file_exists(self):
        lfsf = lfstest('test_fake_file.txt', 'data', 'unit')
        with self.assertRaises(IOError):
            lfsf(dummy)
