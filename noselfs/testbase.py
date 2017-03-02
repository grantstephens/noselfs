import os, shutil, unittest, uuid, tempfile
from .decorator import lfstest


class LfsTestBase(unittest.TestCase):
    def setUp(self):
        # set up temp test directory (sandboxed for each unit test)
        self.testdir = os.path.join(tempfile.gettempdir(),
                                    str(uuid.uuid4()).replace('-', ''))
        if not os.path.exists(self.testdir):
            os.makedirs(self.testdir)

    def tearDown(self):
        # remove temp test directory
        if os.path.exists(self.testdir):
            shutil.rmtree(self.testdir)

    def get_file(self, abs_src, reldest=None):
        if reldest is None or reldest == '':
            reldest = os.path.split(abs_src)[1]

<<<<<<< HEAD
        abs_src = lfstest().lfs_pull(abs_src, reldest)
=======
        abs_src = lfstest().lfs_pull(abs_src)
>>>>>>> 2dca3252450acbbc925c46a17c08c068e4f73247
        abs_dest = os.path.join(self.testdir, reldest)

        dir, ext = os.path.splitext(abs_dest)
        if len(ext) > 0:
            dir = os.path.split(abs_dest)[0]
            if not os.path.exists(dir):
                os.makedirs(dir)
        shutil.copy(abs_src, abs_dest)
        return abs_dest
