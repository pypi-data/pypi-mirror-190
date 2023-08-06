import pyperclip

from dataclasses import dataclass
from kwexception import Kwexception
from short_con import constants
from textwrap import dedent

from .version import __version__

####
# General constants.
####

class CON:
    # Application configuration.
    app_name = 'mvs'
    encoding = 'utf-8'

    # Characters and simple tokens.
    newline = '\n'
    para_break = newline + newline
    space = ' '
    tab = '\t'
    colon = ':'
    period = '.'
    comma_join = ', '
    underscore = '_'
    hyphen = '-'
    dash = hyphen + hyphen
    all = 'all'
    all_tup = (all,)
    yes = 'yes'

    # User-supplied code.
    code_actions = constants('CodeActions', ('rename', 'filter'))
    user_code_fmt = 'def {func_name}(o, p, seq, plan):\n{indent}{user_code}\n'
    func_name_fmt = '_do_{}'

    # Command-line exit codes.
    exit_ok = 0
    exit_fail = 1

    # Logging.
    datetime_fmt = '%Y-%m-%d_%H-%M-%S'
    logfile_ext = 'json'

    # Executables.
    default_pager_cmd = 'more'
    default_copy_cmd = 'pbcopy'
    default_paste_cmd = 'pbpaste'

####
# Structures for input paths data.
####

STRUCTURES = constants('Structures', (
    'paragraphs',
    'flat',
    'pairs',
    'rows',
))

####
# Message formats.
####

MSG_FORMATS = constants('MsgFormats', dict(
    # MvsError instances in RenamingPlan.
    rename_done_already    = 'RenamingPlan cannot rename paths because renaming has already been executed',
    prepare_failed         = 'RenamingPlan cannot rename paths because failures occurred during preparation',
    invalid_control        = 'Invalid problem name(s) for {!r} control: {}',
    conflicting_controls   = 'Conflicting controls for problem {!r}: {!r} and {!r}',
    invalid_file_sys       = 'RenamingPlan.file_sys must be None or an iterable',
    # Error messages in CliRenamer.
    path_collection_failed = 'Collection of input paths failed.\n\n{}',
    plan_creation_failed   = 'Unexpected error during creation of renaming plan.\n\n{}',
    log_writing_failed     = 'Unexpected error during writing to log file.\n\n{}',
    prepare_failed_cli     = 'Renaming preparation resulted in problems:{}.\n',
    renaming_raised        = '\nRenaming raised an error at tracking_index={}. Traceback follows:\n\n{{}}',
    opts_require_one       = 'One of these options is required',
    opts_mutex             = 'No more than one of these options should be used',
    # Other messages in CliRenamer.
    paths_to_be_renamed    = 'Paths to be renamed{}.\n',
    confirm_prompt         = '\nRename paths{}',
    no_action_msg          = '\nNo action taken.',
    paths_renamed_msg      = '\nPaths renamed.',
    cli_version_msg        = f'{CON.app_name} v{__version__}',
))

####
# An exception class for the project.
####

class MvsError(Kwexception):
    pass

####
# A dataclass to hold a pair of paths: original and corresponding new.
####

@dataclass(frozen = True)
class RenamePair:
    # A data object to hold an original path and the corresponding new path.
    orig: str
    new: str
    exclude: bool = False
    create_parent: bool = False
    clobber: bool = False

    @property
    def equal(self):
        return self.orig == self.new

    @property
    def formatted(self):
        return f'{self.orig}\n{self.new}\n'

####
# Read/write: files, clipboard.
####

def read_from_file(path):
    with open(path) as fh:
        return fh.read()

def read_from_clipboard():
    return pyperclip.paste()

def write_to_clipboard(text):
    pyperclip.copy(text)

####
# Other.
####

def positive_int(x):
    # Helper for argparse configuration to check for positive integers.
    if x.isdigit():
        x = int(x)
        if x >= 1:
            return x
    raise ValueError

def wrap_text(text, width):
    # Takes some text and a max width.
    # Wraps the text to the desired width and returns it.

    # Convenience vars.
    NL = CON.newline
    SP = CON.space

    # Split text into words. If none, return immediately.
    words = [
        w
        for line in text.split(NL)
        for w in line.strip().split(SP)
    ]
    if not words: # pragma: no cover
        return ''

    # Assemble the words into a list-of-list, where each
    # inner list will become a line within the width limit.
    lines = [[]]
    tot = 0
    for w in words:
        n = len(w)
        if n == 0: # pragma: no cover
            continue
        elif tot + n + 1 <= width:
            lines[-1].append(w)
            tot += n + 1
        else:
            lines.append([w])
            tot = n

    # Join the words back into a paragraph of text.
    return NL.join(
        SP.join(line)
        for line in lines
    )

