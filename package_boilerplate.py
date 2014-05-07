import sublime, sublime_plugin
import re
import os
import codecs
import shutil

import sys, glob
from imp import reload

# Reload tests
for test_file in glob.glob("tests/test_*.py"):
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

    def packages_path(self):
        return self.settings.get("packages_path", False) or sublime.packages_path()

    def show_input_panel(self, caption, on_done = None, on_change = None, on_cancel = None):
        sublime.active_window().show_input_panel(caption, "", on_done, on_change, on_cancel)

class PackageSkeleton():
    def __init__(self, skeleton_folder_path):
        self.skeleton_folder_path = skeleton_folder_path

    def compose(self, package_name, destination):
        package_destination = os.path.join(destination, package_name)
        self.ensure_directory(package_destination)
        self.copy_files(package_destination, package_name)

    def copy_files(self, destination, package_name):
        for file_path in os.listdir(self.skeleton_folder_path):
            skeleton_file = os.path.join(self.skeleton_folder_path, file_path)
            new_file = os.path.join(destination, self.replace_file_name(file_path, package_name))
            shutil.copy(skeleton_file, new_file)
            self.replace_contents(new_file, package_name)

    def replace_file_name(self, file_name, package_name):
        return file_name.replace("PackageName", package_name).replace("package_name", self.to_underscore(package_name))

    def replace_contents(self, file_path, package_name):
        with codecs.open(file_path, 'r+', "utf-8") as opened_file:
            file_content = opened_file.read()
            try:
                new_content = file_content.format(package_name = package_name)
            except KeyError:
                new_content = file_content

            self.write_text(opened_file, new_content)

    def write_text(self, file_to_write, text):
        file_to_write.seek(0)
        file_to_write.write(text)
        file_to_write.truncate()

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def to_underscore(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()