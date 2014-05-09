import sublime

is_sublime_text_3 = int(sublime.version()) >= 3000

if is_sublime_text_3:
    from .base_command import BaseCommand
else:
    from base_command import BaseCommand
    
class ExampleCommand(BaseCommand):
    def work(self):
        pass