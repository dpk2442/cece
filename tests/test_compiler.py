"""
.. module tests.test_compiler

Test the Compiler class in cece.compiler
"""

import cece.compiler
import mock
import os
import unittest


class TestMakeIdUrl(unittest.TestCase):
    """ Test ``cece.compiler.Compiler._make_id_url`` """

    def setUp(self):
        """ Set up for each test. """

        self._compiler = cece.compiler.Compiler(None, None)

    def testNoBackslash(self):
        """ Test the case with no backslash. """

        result = self._compiler._make_id_url("test/one")
        self.assertEqual(result, "/test/one/")

    def testBackslash(self):
        """ Test the case with a backslash. """

        result = self._compiler._make_id_url("test\\one")
        self.assertEqual(result, "/test/one/")


class TestCompile(unittest.TestCase):
    """ Test ``cece.compiler.Compiler.compile`` """

    @mock.patch("cece.compiler.open", create=True)
    @mock.patch("cece.compiler.cece.util.makedirs")
    @mock.patch("cece.compiler.shutil")
    @mock.patch("cece.compiler.os")
    def testSuccess(self, mock_os, mock_shutil, mock_makedirs, mock_open):
        """ Test the compile method for the success case. """

        starting_dir = os.sep

        config = {"site_title": "Test Site"}
        guides = {
            "": {"type": "folder"},
            "folder1": {"type": "folder"},
            "folder1/page1": {"type": "page", "source_path": "page1"},
            "folder1/folder2": {"type": "folder"},
            "folder1/folder2/page2": {"type": "page", "source_path": "page2"},
            "folder3": {"type": "folder"},
            "folder3/page3": {"type": "page", "source_path": "page3"}
        }

        mock_os.path.isdir.return_value = True
        mock_os.path.join = os.path.join
        mock_os.getcwd.return_value = starting_dir

        compiler = cece.compiler.Compiler(config, guides)
        compiler.compile()

        # check build dir is found and deleted
        mock_os.path.isdir.assert_called_once_with("build")
        mock_shutil.rmtree.assert_called_once_with("build")

        # check build dir is created again
        mock_os.mkdir.assert_any_call("build")

        # check folders are created
        mock_makedirs.assert_any_call("folder1")
        mock_makedirs.assert_any_call("folder1/folder2")
        mock_makedirs.assert_any_call("folder3")

        # check files are opened for read and write
        mock_open.assert_any_call("page1", "r")
        mock_open.assert_any_call("page2", "r")
        mock_open.assert_any_call("page3", "r")
        mock_open.assert_any_call(os.path.join("folder1/page1", "index.html"), "w")
        mock_open.assert_any_call(os.path.join("folder1/folder2/page2", "index.html"), "w")
        mock_open.assert_any_call(os.path.join("folder3/page3", "index.html"), "w")
