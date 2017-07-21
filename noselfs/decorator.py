from functools import wraps
from nose.plugins.attrib import attr

import os
import pkg_resources
import shlex
import subprocess


class lfstest(object):
    def __init__(self, file_name=None, data_dir=None, test_type=None,
                 *args, **kwargs):
        self.named_attrib = kwargs
        self.named_attrib['type'] = test_type
        self.attrib = args
        self.file_name = file_name
        self.data_dir = data_dir

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
                    output.append(
                        self._get_file(file_n, self.data_dir,
                                       self.named_attrib['type'], mod))
                self.file_name = output
            else:
                self.file_name = self._get_file(
                    self.file_name, self.data_dir,
                    self.named_attrib['type'], mod)
            file_name_pass = self.file_name
        else:
            file_name_pass = None

        @attr(*self.attrib, **self.named_attrib)
        @wraps(f)
        def wrapper(self, *args, **kwargs):

            if file_name_pass is None:
                return f(self, *args, **kwargs)
            else:
                return f(self, file_name_pass, *args, **kwargs)

        return wrapper

    def _get_file(self, file_name, data_dir, test_type, mod):
        if data_dir is None:
            data_dir = ''
        if test_type is None:
            test_type = ''
        file_name_relative = os.path.join(data_dir, test_type, file_name)
        file_name = pkg_resources.resource_filename(
            mod, file_name_relative
        )

        return self.lfs_pull(file_name, file_name_relative)

    def lfs_pull(self, file_name, file_name_relative):
        if not os.path.isfile(file_name):
            raise IOError('Filename or Pointer ({}) is not available.'.format(
                file_name))
        elif os.path.getsize(file_name) < 300:
            with open(file_name) as open_file:
                if (('version' in open_file.read()) &
                        ('size' in open_file.read()) &
                        ('oid' in open_file.read())):
                    process = subprocess.Popen(
                        shlex.split(
                            'git lfs pull --include="{}" --exclude=""'.format(
                                os.path.join('**', file_name_relative))),
                        stdout=subprocess.PIPE
                    )
                    output, error = process.communicate()
                    if error is not None:
                        raise Exception(
                            'Tried LFS pull. Failed with: {}'.format(error)
                        )
        return file_name
