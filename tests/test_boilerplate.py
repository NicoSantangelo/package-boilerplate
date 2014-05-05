import unittest
from PackageBoilerplate import package_boilerplate

# Remember: 
#   Install AAAPT package to run the tests
#   Save package_boilerplate to reload the tests

class Test_PackageBoilerplate(unittest.TestCase):
    def test_it_filters_the_closed_elements(self):
        self.assertEqual(2, 2)