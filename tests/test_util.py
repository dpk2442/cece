"""
.. module tests.test_util

Test the functions in cece.util
"""

import cece.util
import mock
import unittest
import yaml


class TestLoadYamlFile(unittest.TestCase):
    """ Test ``cece.util.load_yaml_file`` """

    @mock.patch("cece.util.yaml.load")
    @mock.patch("cece.util.open")
    def test_success(self, mock_open, mock_yaml_load):
        """
            Test the success case where the file opens as expected, and parsing
            raises no errors.
        """

        test_dict = {"test": "test_value"}

        # mock the functions
        mock_open.return_value = mock.MagicMock(spec=file)
        mock_yaml_load.return_value = test_dict

        # call the method to test
        returned_dict = cece.util.load_yaml_file("test_file")

        # verify the right methods were called and the return value is correct
        mock_open.assert_called_once_with("test_file", "r")
        mock_opened_file = mock_open.return_value.__enter__.return_value
        mock_yaml_load.assert_called_once_with(mock_opened_file)
        self.assertEqual(test_dict, returned_dict)

    @mock.patch("cece.util.sys.exit")
    @mock.patch("cece.util.print")
    @mock.patch("cece.util.yaml.load")
    @mock.patch("cece.util.open")
    def test_yaml_error(self, mock_open, mock_yaml_load, mock_print, mock_exit):
        """
            Test the case where the yaml parsing raises and error.
        """

        yaml_error = yaml.YAMLError("yaml error")

        # mock the functions
        mock_open.return_value = mock.MagicMock(spec=file)
        mock_yaml_load.side_effect = yaml_error

        # call the method
        cece.util.load_yaml_file("test_file")

        # verify the call
        mock_open.assert_called_once_with("test_file", "r")
        mock_opened_file = mock_open.return_value.__enter__.return_value
        mock_yaml_load.assert_called_once_with(mock_opened_file)
        mock_print.assert_any_call("Error parsing \"test_file\":")
        mock_print.assert_any_call(yaml_error)
        mock_exit.assert_called_once_with(1)


class TestNaturalSort(unittest.TestCase):
    """ Test ``cece.util.natural_sort`` """

    def test_alpha(self):
        """
            Test sorting strings of all letters.
        """

        lst = ["toast", "test", "alpha", "word"]
        cece.util.natural_sort(lst)
        self.assertEqual(["alpha", "test", "toast", "word"], lst)

    def test_numeric(self):
        """
            Test sorting strings of all numbers.
        """

        lst = ["8", "4", "101", "3", "10"]
        cece.util.natural_sort(lst)
        self.assertEqual(["3", "4", "8", "10", "101"], lst)

    def test_alphanumeric(self):
        """
            Test sorting strings of letters and numbers.
        """

        lst = ["test21", "test10", "test2", "test1"]
        cece.util.natural_sort(lst)
        self.assertEqual(["test1", "test2", "test10", "test21"], lst)


class TestMakedirs(unittest.TestCase):
    """ Test ``cece.util.makedirs`` """

    @mock.patch("cece.util.os")
    def test_new_dir(self, mock_os):
        """
            Test the case where the directory does not already exist.
        """

        mock_os.path.isdir.return_value = False

        cece.util.makedirs("test dirs")

        mock_os.path.isdir.assert_called_once_with("test dirs")
        mock_os.makedirs.assert_called_once_with("test dirs")

    @mock.patch("cece.util.os")
    def test_existing_dir(self, mock_os):
        """
            Test the case where the directory already exists.
        """

        mock_os.path.isdir.return_value = True

        cece.util.makedirs("test dirs")

        mock_os.path.isdir.assert_called_once_with("test dirs")
        mock_os.makedirs.assert_not_called()


class TestIterateListSubsets(unittest.TestCase):
    """ Test ``cece.util.iterate_list_subsets`` """

    def test_empty(self):
        """
            Test the empty list.
        """

        lst = []
        actual = list(cece.util.iterate_list_subsets(lst))
        self.assertEqual(
            [], actual,
            "No iterations should occur on an empty list.")

    def test_normal(self):
        """
            Test a standard list.
        """

        lst = [0, 1, 2]
        expected = [[0], [0, 1], [0, 1, 2]]
        actual = list(cece.util.iterate_list_subsets(lst))
        self.assertEqual(expected, actual)
