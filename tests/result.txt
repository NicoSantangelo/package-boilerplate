import sublime, sublime_plugin

is_sublime_text_3 = int(sublime.version()) >= 3000

if is_sublime_text_3:
    from .progress_notifier import ProgressNotifier
else:
    from progress_notifier import ProgressNotifier

class BaseCommand(sublime_plugin.TextCommand):
    package_name = "SuperPackage"

    def run(self, edit):
        self.setup_data_from_settings()
        self.work()

    def setup_data_from_settings(self):
        self.settings = sublime.load_settings(self.package_name + ".sublime-settings")

    # Main method, override
    def work(self):
        pass
