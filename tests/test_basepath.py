import sublime
import unittest

from PackageBoilerplate import package_boilerplate

# Remember: 
#   Install AAAPT package to run the tests
#   Save package_boilerplate to reload the tests

class Test_BasePath(unittest.TestCase):
    def test_join_combines_the_packages_path_with_the_supplied_one(self):
        result = package_boilerplate.BasePath.join("some/new/path")
        self.assertEquals(result, sublime.packages_path() + "/PackageBoilerplate/some/new/path")