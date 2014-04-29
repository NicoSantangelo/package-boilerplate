import sublime, sublime_plugin

class PackageGeneratorCommand(sublime_plugin.WindowCommand):
    def run(self):
        # TODO:
        # Ask for user options (or hardcode them in settings), like "Want to use a progress bar?"
        # Use sublime.packages_path() or a hardcoded option as destination.
        # Create the package files. Figure out the best way to replace the project specific options (like file names and Menu).
        pass