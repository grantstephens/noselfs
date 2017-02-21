from functools import wraps
from nose.plugins.attrib import attr
from nose.tools import nottest
import os
import pkg_resources
import shlex
import subprocess
import traceback


class lfstest(object):
    def __init__(self, test_type, file_name=None, *args, **kwargs):
        self.named_attrib = kwargs
        self.named_attrib['type'] = test_type
        self.attrib = args
        self.file_name = file_name

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        mod = f.__module__
        if self.file_name is not None:
            if isinstance(self.file_name, list):
                output = []
                for file_n in self.file_name:
                    output.append(self._get_file(file_n, self.named_attrib['type'], mod))
                self.file_name = output
            else:
                self.file_name = self._get_file(self.file_name, self.named_attrib['type'], mod)

        def wrapped_f(*args):

            @attr(*self.attrib, **self.named_attrib)
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                if self.file_name is None:
                    return f(self, *args, **kwargs)
                else:
                        return f(self, self.file_name, *args, **kwargs)
        return wrapped_f

    def _get_file(self, file_name, test_type, mod):
        file_name_relative = os.path.join('data', test_type, file_name)
        file_name = pkg_resources.resource_filename(
            mod, file_name_relative
            )
        if not os.path.isfile(file_name):
            raise IOError('Filename or Pointer not available.')
        elif os.path.getsize(file_name) < 300:
            with open(file_name) as open_file:
                check_words = [next(open_file).split(' ')[0] for x in xrange(3)]
            if all(word in check_words for word in ['version', 'size', 'oid']):
                process = subprocess.Popen(
                    shlex.split('git lfs pull --include="{}" --exclude=""'.format(
                        os.path.join('tests', file_name_relative))),
                    stdout=subprocess.PIPE
                    )
                output, error = process.communicate()
                if error is not None:
                    raise Exception(
                        'Tried LFS pull. Failed with: {}'.format(error)
                        )
        return file_name

# @nottest
# def lfstest(test_type, file_name=None, *args, **kwargs):
#     """
#     A wrapper to wrap all tests. It will also add any nose attributes that you
#         give it.
#     :param type: string- The type of test, be it unit, integration or model
#     :param file_name: The file name needed as input to the test. This will
#         get the file from LFS if it isn't available. Can also be a list of file
#         names.
#     :return file_name: The absolute path of the file_name given as input. If
#         list is give a list will be returned.
#     """
#     named_attrib = kwargs
#     named_attrib['type'] = test_type
#     attrib = args
#     # fff = file_name
#
#     def real_decorator(f, **kwargs):
#
#
#         print file_name
#         @attr(*attrib, **named_attrib)
#         @wraps(f)
#         def wrapper(self, *args, **kwargs):
#             # if file_name is not None:
#             #     if isinstance(file_name, list):
#             #         output = []
#             #         for file_n in file_name:
#             #             output.append(_get_file(file_n))
#             #         file_name = output
#             #     else:
#             #         file_name = _get_file(file_name, test_type)
#             # print file_name
#
#             if file_name is None:
#                 return f(self, *args, **kwargs)
#             else:
#                 return f(self, *args, unit_test_file=file_name, **kwargs)
#         return wrapper
#     return real_decorator
#
#
# def _get_file(file_name, test_type):
#     file_name_relative = os.path.join('data', test_type, file_name)
#     file_name = pkg_resources.resource_filename(
#         __name__, file_name_relative
#         )
#     print file_name
#     if not os.path.isfile(file_name):
#         raise IOError('Filename or Pointer not available.')
#     elif os.path.getsize(file_name) < 300:
#         with open(file_name) as open_file:
#             check_words = [next(open_file).split(' ')[0] for x in xrange(3)]
#         if all(word in check_words for word in ['version', 'size', 'oid']):
#             process = subprocess.Popen(
#                 shlex.split('git lfs pull --include="{}" --exclude=""'.format(
#                     os.path.join('tests', file_name_relative))),
#                 stdout=subprocess.PIPE
#                 )
#             output, error = process.communicate()
#             if error is not None:
#                 raise Exception(
#                     'Tried LFS pull. Failed with: {}'.format(error)
#                     )
#     return file_name
