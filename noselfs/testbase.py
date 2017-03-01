import os, errno, stat, shutil, unittest, uuid, tempfile
from .decorator import lfstest


class LfsTestBase(unittest.TestCase):
    def setUp(self):
        # set up temp test directory (sandboxed for each unit test)
        self.testdir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()).replace('-', ''))
        if not os.path.exists(self.testdir):
            os.makedirs(self.testdir)

    def tearDown(self):
        # remove temp test directory
        if os.path.exists(self.testdir):
            shutil.rmtree(self.testdir, ignore_errors=False, onerror=handle_remove_readonly)

    def get_file(self, abs_src, reldest):
        abs_src = lfstest().lfs_pull(abs_src)
        abs_dest = os.path.join(self.testdir, reldest)

        dir, ext = os.path.splitext(abs_dest)
        if len(ext) > 0:
            dir = os.path.split(abs_dest)[0]
            if not os.path.exists(dir):
                os.makedirs(dir)
        shutil.copy(abs_src, abs_dest)
        return abs_dest


def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise
