from noselfs import lfstest
import unittest
import os
import pkg_resources


def dummy(self, file_name):
    return file_name


class TestNoseLFSDecorator(unittest.TestCase):

    def test_file_name(self):
        lfsf = lfstest('test_file.txt', 'data', 'unit')
        lfsf(dummy)
        file_name_relative = os.path.join('data', 'unit', 'test_file.txt')
        file_name = pkg_resources.resource_filename(
            __name__, file_name_relative
            )
        self.assertEqual(lfsf.file_name, file_name)

    def test_file_name_no_space(self):
        lfsf = lfstest('test_file_2.txt', 'data', 'unit')
        lfsf(dummy)
        file_name_relative = os.path.join('data', 'unit', 'test_file_2.txt')
        file_name = pkg_resources.resource_filename(
            __name__, file_name_relative
            )
        self.assertEqual(lfsf.file_name, file_name)

    def test_file_exists(self):
        lfsf = lfstest('test_fake_file.txt', 'data', 'unit')
        with self.assertRaises(IOError):
            lfsf(dummy)

    def test_file_pull(self):
        lfsf = lfstest('fake_pointer.txt', 'data', 'unit')
        file_name = lfsf(dummy)
        file_name('sometext')
