import sublime, sublime_plugin

is_sublime_text_3 = int(sublime.version()) >= 3000

class BaseCommand(sublime_plugin.TextCommand):
    package_name = "{PackageName}"

    def run(self, edit = None):
        self.setup_data_from_settings()
        self.work()

    def setup_data_from_settings(self):
        self.settings = sublime.load_settings(self.package_name + ".sublime-settings")

    # Main method, override
    def work(self):
        pass

    # Panels and message
    def display_message(self, text):
        sublime.active_window().active_view().set_status(self.package_name, text)

    def show_quick_panel(self, items, on_done = None):
        self.defer_sync(lambda: sublime.active_window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT))

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        sublime.active_window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)

    # Output view
    def show_output_panel(self, text):
        output_panel_name = self.package_name.lower() + "_output"
        self.scroll_to_end = True
        self.output_view = sublime.active_window().get_output_panel(output_panel_name)
        sublime.active_window().run_command("show_panel", { "panel": "output." + output_panel_name })
        self.append_to_output_view(text)

    def ouput_in_new_tab(self, text):
        self.scroll_to_end = False
        self.output_view = sublime.active_window().open_file(self.package_name + " Results")
        self.append_to_output_view(text)

    def append_to_output_view(self, text):
        self.output_view.set_read_only(False)
        self._insert(self.output_view, text)
        self.output_view.set_read_only(True)

    def _insert(self, view, content):
        view.run_command("view_insert", { "size": view.size(), "content": content })
        position = (view.size(), view.size()) if self.scroll_to_end else (0, 0)
        view.set_viewport_position(position, True)

    # Async calls
    def defer_sync(self, fn):
        sublime.set_timeout(fn, 0)

    def defer(self, fn):
        self.async(fn, 0)
        
    def async(self, fn, delay):
        if is_sublime_text_3:
            # You can add support/progress_notifier and use it here to show a progress bar
            sublime.set_timeout_async(lambda: self.call(fn), delay)
        else:
            fn()

    def call(self, fn, progress = None):
        fn()
        if progress:
            progress.stop()

class ViewInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, size, content):
        self.view.insert(edit, size, content)