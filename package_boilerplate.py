import sublime, sublime_plugin
import re
import os
import codecs
import fnmatch
import shutil

import sys, glob
from imp import reload

# Reload tests
for test_file in glob.glob("tests/test_*.py"):
    key = "PackageBoilerplate." + test_file[:-3].replace("/", ".")
    if key in sys.modules:
        reload(sys.modules[key])

class PackageBoilerplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("PackageBoilerplate.sublime-settings")
        self.show_input_panel("Package name", self.name_input_callback)

    def name_input_callback(self, package_name):
        if not package_name:
            sublime.active_window().active_view().set_status("PackageBoilerplate", "Please supply a name for your package!") 
            return

        PackageSkeleton("skeleton").compose(package_name, self.packages_path())

    def packages_path(self):
        return self.settings.get("packages_path", False) or sublime.packages_path()

    def show_input_panel(self, caption, on_done = None, on_change = None, on_cancel = None):
        sublime.active_window().show_input_panel(caption, "", on_done, on_change, on_cancel)

class PackageSkeleton():
    def __init__(self, skeleton_folder_path, skip = []):
        self.skeleton_folder_path = skeleton_folder_path
        self.skip = skip

    def compose(self, package_name, destination):
        package_destination = os.path.join(destination, package_name)
        self.ensure_directory(package_destination)
        self.copy_files(package_destination, package_name)

    def copy_files(self, destination, package_name, folder_to_list = None):
        folder_to_list = folder_to_list or self.skeleton_folder_path
        for file_path in os.listdir(folder_to_list):
            skeleton_file = os.path.join(folder_to_list, file_path)
            new_file_name = self.replace_file_name(file_path, package_name)
            if not self.should_skip(new_file_name):
                new_destination = os.path.join(destination, new_file_name)
                if os.path.isfile(skeleton_file):
                    self.copy_file(skeleton_file, new_destination, package_name)
                else:
                    self.ensure_directory(new_destination)
                    self.copy_files(new_destination, package_name, skeleton_file)

    def copy_file(self, source, destination, package_name):
        shutil.copy(source, destination)
        self.replace_contents(destination, package_name)

    def should_skip(self, file_name):
        for skip_wildcard in self.skip:
            if fnmatch.fnmatch(file_name, skip_wildcard):
                return True
        return False

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