import sublime
import sublime_plugin

from GitGutter.git_gutter_handler import GitGutterHandler
PPA_MODULE = __import__("Python PEP8 Autoformat").pep8_autoformat

autopep8 = PPA_MODULE.autopep8
MergeUtils = PPA_MODULE.MergeUtils

SETTINGS_FILE = 'python_diff_formatter.sublime-settings'


class PythonPEP8AutoformatSettingsParser(object):

    def __init__(self):
        self.settings = sublime.load_settings(SETTINGS_FILE)

    def get_options(self, diff=None):
        cmd_args = list()
        cmd_args.extend(['--aggressive'] * self.settings.get('aggressive', 0))
        if self.settings.get('list-fixes', False):
            cmd_args.append('--list-fixes')
        if self.settings.get('ignore', False):
            cmd_args.append('--ignore={0}'.format(','.join(
                [o.strip() for o in self.settings.get('ignore') if o.strip()])))
        if self.settings.get('select', False):
            cmd_args.append('--select={0}'.format(','.join(
                [o.strip() for o in self.settings.get('select') if o.strip()])))
        if self.settings.get('max-line-length', False):
            cmd_args.append('--max-line-length={0}'.format(
                self.settings.get('max-line-length')))
        if self.settings.get('indent-size', False):
            cmd_args.append('--indent-size={0}'.format(
                self.settings.get('indent-size')))
        if diff:
            cmd_args.extend(['--line-range', str(diff[0]), str(diff[1])])

        # -- We must give a filename to pass the parse_args() tests
        cmd_args.append('filename')
        options = autopep8.parse_args(cmd_args)

        return options


def get_diff_set(change_set):
    lines = [item for sublist in change_set for item in sublist]
    lines.sort()

    if not lines:
        return []

    regions = []
    current_start = lines[0]
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1] + 1:
            continue

        regions.append((current_start, lines[i - 1]))
        current_start = lines[i]

    regions.append((current_start, lines[-1]))
    return regions


class PythonDiffFormatCommand(sublime_plugin.TextCommand):

    def _run_for_diff(self, edit, source, diff):
        fixed = autopep8.fix_code(source, options=PPA.get_options(diff=diff))
        is_dirty, err = MergeUtils.merge_code(self.view, edit, source, fixed)
        if err:
            sublime.error_message(
                "%s: Merge failure: '%s'" % (PLUGIN_NAME, err))
            raise

    def run(self, edit):
        syntax = self.view.settings().get('syntax')
        if syntax.lower().find('python') == -1:
            return

        git_gutter_handler = GitGutterHandler(self.view)
        diff_set = get_diff_set(git_gutter_handler.diff())

        for diff in diff_set[::-1]:
            replace_region = self.view.line(
                sublime.Region(0, self.view.size()))
            source = self.view.substr(replace_region)
            self._run_for_diff(edit, source, diff)

    def is_visible(self, *args):
        return True


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        syntax = view.settings().get('syntax')
        if syntax.lower().find('python') == -1:
            return

        # do autoformat on file save if allowed in settings
        if PPA.settings.get('autoformat_on_save', False):
            view.run_command('python_diff_format')


def plugin_loaded():
    global PPA
    PPA = PythonPEP8AutoformatSettingsParser()
