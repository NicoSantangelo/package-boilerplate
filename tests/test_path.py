import sublime
import unittest
import os

from PackageBoilerplate import package_boilerplate

# Remember: 
#   Install AAAPT package to run the tests
#   Save package_boilerplate to reload the tests

class SettingsMock():
    def __init__(self, settings):
        self.settings = settings

    def get(self, key, fallback):
        return self.settings[key] if key in self.settings else fallback

class Test_Path(unittest.TestCase):
    def setUp(self):
        self.sublime_error_message = sublime.error_message
        sublime.error_message = lambda str: None
        self.settings = SettingsMock({ "path": "skeleton", "wrongpath": "some/other/path" })
        self.path = package_boilerplate.Path(self.settings)

    def test_get_returns_the_path_from_the_settings(self):
        self.assertEquals(self.path.get("path"), "skeleton")

    def test_get_returns_the_fallback_if_the_key_isnt_found_in_the_settings(self):
        self.assertEquals(self.path.get("nonsense", "support"), "support")

    def test_get_throws_if_the_path_doesnt_exist(self):
        self.assertRaises(FileNotFoundError, lambda: self.path.get("wrongpath"))
        self.assertRaises(FileNotFoundError, lambda: self.path.get("nonsense", "morenonsense"))

    def tearDown(self):
        sublime.error_message = self.sublime_error_message