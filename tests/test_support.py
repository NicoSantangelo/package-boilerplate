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
        self.assertEquals(self.package_support.items(), ["All: Add all support",
            "BaseCommand: A base class for sublime commands",
            "ProgressNotifier: Add a progress bar a la 'Package Control'",
            "Tests: Add test structure (using the AAAPT package)",
            "What's this?",
            "Exit"
        ])

    def test_support_actions_returns_all_the_non_extra_actions(self):
        self.package_support.options = [
            { 'name': "NotExtra", 'action': "NotExtraAction" },
            { 'name': "Extra", 'action': "ExtraAction", 'extra': True }
        ]
        self.assertEquals(self.package_support.support_actions(), ["NotExtraAction"])

    def test_support_actions_skips_the_add_all_method(self):
        self.package_support.options = [
            { 'name': "NotExtra", 'action': "NotExtraAction" },
            { 'name': "Add all", 'action': self.package_support.add_all },
        ]
        self.assertEquals(self.package_support.support_actions(), ["NotExtraAction"])

    def test_is_extra_returns_True_if_extra_exists_in_the_dict_and_is_True(self):
        self.assertTrue(self.package_support.is_extra({ 'extra': True }))
        self.assertFalse(self.package_support.is_extra({ 'extra': False }))
        self.assertFalse(self.package_support.is_extra({ 'something': True }))