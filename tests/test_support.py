import unittest

from PackageBoilerplate import package_boilerplate

# Remember: 
#   Install AAAPT package to run the tests
#   Save package_boilerplate to reload the tests

class Test_PackageBoilerplateSupportCommand(unittest.TestCase):
    def setUp(self):
        self.package_support = package_boilerplate.PackageBoilerplateSupportCommand({})
        self.package_support.show_quick_panel = lambda x, y: None

    def test_items_returns_the_name_of_the_available_options(self):
        self.package_support.run()
        self.assertEquals(self.package_support.items(), ["All: Add all support", "BaseCommand: A base class for sublime commands", "ProgressNotifier: Add a progress bar a la 'Package Control'", "What's this?", "Exit"])
