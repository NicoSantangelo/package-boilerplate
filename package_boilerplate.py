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

# Commands

class PackageBoilerplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("PackageBoilerplate.sublime-settings")
        self.cache_paths()
        self.show_input_panel("Package name", on_done = self.name_input_callback, on_cancel = self.name_input_callback)

    # Cache the paths so we can throw an error (if there is any) before asking for the package name
    def cache_paths(self):
        path = Path(self.settings)
        self.skeleton_path = path.get("base_package_structure_path", BasePath.join("skeleton"))
        self.packages_path = path.get("packages_path", sublime.packages_path())

    def name_input_callback(self, package_name = None):
        if not package_name:
            self.set_status("Please supply a name for your package!")
            return

        PackageSkeleton(package_name).compose(self.skeleton_path, self.packages_path)

    def show_input_panel(self, caption, on_done = None, on_change = None, on_cancel = None):
        sublime.active_window().show_input_panel(caption, "", on_done, on_change, on_cancel)

    def set_status(self, text):
        sublime.active_window().active_view().set_status("PackageBoilerplate", text) 


class PackageBoilerplateSupportCommand(sublime_plugin.WindowCommand):
    def run(self):
        # TODO:
        # 'all' option
        # Package list instead of asking for the name
        # Support for testing
        # Remove imports from BaseCommand
        self.options = [
            { 'name': "All: Add all support", 'action': self.add_all },
            { 'name': "BaseCommand: A base class for sublime commands", 'action': self.add_base_command },
            { 'name': "ProgressNotifier: Add a progress bar a la 'Package Control'", 'action': self.add_progress_notifier },
            { 'name': "What's this?", 'action': self.explain, 'extra': True },
            { 'name': "Exit", 'action': lambda : None, 'extra': True }
        ]
        self.settings = sublime.load_settings("PackageBoilerplate.sublime-settings")
        self.packages_path = Path(self.settings).get("packages_path", sublime.packages_path())
        self.show_quick_panel(self.items(), self.callback)

    def items(self):
        return [option['name'] for option in self.options]

    def callback(self, index):
        option = self.options[index]
        if not option is None:
            if 'extra' in option and option['extra']:
                option['action']()
            else:
                self.ask_package_name(option['action'])

    def add_all(self, package_name = None):
        pass

    def add_base_command(self, package_name = None):
        self._copy_support_file(package_name, "base_command.py")

    def add_progress_notifier(self, package_name = None):
        self._copy_support_file(package_name, "progress_notifier.py")

    def _copy_support_file(self, package_name, file_name):
        if not package_name:
            return
        support_file_path = BasePath.join("support", file_name)
        package_path = os.path.join(self.packages_path, package_name, file_name)
        PackageSkeleton(package_name).copy_file(support_file_path, package_path)

    def explain(self):
        self.window.open_file(BasePath.join("support", "Explanation.txt"))

    def ask_package_name(self, callback):
        subl_path = sublime.packages_path()
        package_names = [name for name in os.listdir(subl_path) if os.path.isdir(os.path.join(subl_path, name))]
        def callback_wrap(index):
            if index >= 0 and index < len(package_names):
                callback(package_names[index])
        self.show_quick_panel(package_names, callback_wrap)

    def show_quick_panel(self, items, on_done = None, on_highlighted = None, selected_index = -1):
        sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, selected_index, on_highlighted), 0)


# Custom Classes

class BasePath():
    base = os.path.join(sublime.packages_path(), "PackageBoilerplate")

    @classmethod
    def join(cls, *paths):
        return os.path.join(cls.base, *paths)

class Path():
    def __init__(self, settings):
        self.settings = settings

    def get(self, settings_key, fallback = None):
        path = self.settings.get(settings_key, False) or fallback
        if not os.path.exists(path):
            sublime.error_message("PackageBoilerplate\nTried to use the path " + path + " to create the files, but it wasn't found.\nCheck your settings or create an issue on this package repository")
            raise FileNotFoundError(path)
        return path

class PackageSkeleton():
    def __init__(self, package_name, skip = []):
        self.package_name = package_name
        self.underscore_package_name = self.to_underscore(package_name)
        self.skip = skip

    def compose(self, source, destination):
        package_destination = os.path.join(destination, self.package_name)
        self.ensure_directory(package_destination)
        self.copy_files(source, package_destination)

    def copy_files(self, source, destination):
        for file_path in os.listdir(source):
            skeleton_file = os.path.join(source, file_path)
            new_file_name = self.replace_file_name(file_path)
            if not self.should_skip(new_file_name):
                new_destination = os.path.join(destination, new_file_name)
                self.copy_file(skeleton_file, new_destination)

    def copy_file(self, source, destination):
        if os.path.isfile(source):
            shutil.copy(source, destination)
            self.replace_contents(destination)
        else:
            self.ensure_directory(destination)
            self.copy_files(source, destination)

    def should_skip(self, file_name):
        for skip_wildcard in self.skip:
            if fnmatch.fnmatch(file_name, skip_wildcard):
                return True
        return False

    def replace_file_name(self, file_name):
        return file_name.replace("PackageName", self.package_name).replace("package_name", self.underscore_package_name)

    def replace_contents(self, file_path):
        with codecs.open(file_path, 'r+', "utf-8") as opened_file:
            new_content = opened_file.read().replace("{package_name}", self.package_name)
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