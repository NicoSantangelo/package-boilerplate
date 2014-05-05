import sublime, sublime_plugin
import os

import sys, glob
from imp import reload

# Reload tests
for test_file in glob.glob("tests/*.py"):
    reload(sys.modules["PackageBoilerplate." + test_file[:-3].replace("/", ".")])

class PackageBoilerplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        # TODO:
        # Create the package files. Figure out the best way to replace the project specific options (like file names and Menu).
        # Check for skip (BaseCommand, ProgressNotifier, messages) in the settings

        self.settings = sublime.load_settings("PackageBoilerplate.sublime-settings")
        self.show_input_panel("Package name", self.name_input_callback)

    def name_input_callback(self, package_name):
        if not package_name:
            sublime.active_window().active_view().set_status("PackageBoilerplate", "Please supply a name for your package!") 
            return

        package_destination = os.path.join(self.packages_path(), package_name)
        self.ensure_directory(package_destination)

    def packages_path(self):
        return self.settings.get("packages_path", False) or sublime.packages_path()

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def show_input_panel(self, caption, on_done = None, on_change = None, on_cancel = None):
        sublime.active_window().show_input_panel(caption, "", on_done, on_change, on_cancel)