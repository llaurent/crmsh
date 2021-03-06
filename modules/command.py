# Copyright (C) 2013 Kristoffer Gronlund <kgronlund@suse.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# - Base class for UI levels
# - Decorators and other helper functions for the UI
#   Mostly, what these functions do is store extra metadata
#   inside the functions.

import inspect
from . import help as help_module
from . import ui_utils
from .msg import common_debug


def name(n):
    '''
    Overrides the name of the command.
    This is useful to handle commands with
    dashes instead of underlines, or commands
    with awkward names (like commands with a
    leading underscore).
    '''
    def inner(fn):
        setattr(fn, '_name', n)
        return fn
    return inner


def alias(*aliases):
    '''
    Adds aliases for the command. The command
    will also be callable using the alias. The
    command name set in the command context will
    reflect the alias used (so the same command can
    behave differently depending on the alias).
    '''
    def inner(fn):
        setattr(fn, '_aliases', aliases)
        return fn
    return inner


def level(level_class):
    '''
    Changes the command into a level movement.
    Calling the command doesn't actually call the
    member function this decorator is applied to, so
    don't put any code in that function.

    This is a bit awkward, but given how decorators work,
    it's the best I could think of.
    '''
    def inner(fn):
        # check signature of given level function
        _check_args(fn, ('self',))

        setattr(fn, '_ui_type', 'level')
        setattr(fn, '_level', level_class)

        def default(arg, val):
            if not hasattr(fn, arg):
                setattr(fn, arg, val)

        default('_aliases', tuple())
        default('_short_help', None)
        default('_long_help', None)
        return fn
    return inner


def help(doc):
    '''
    Use to set a help text for a command or level
    which isn't documented in crm.8.adoc.

    The first line of the doc string will be used as
    the short help, the rest will be used as the full
    help message.
    '''
    doc_split = doc.split('\n', 1)

    def inner(fn):
        setattr(fn, '_short_help', doc_split[0])
        if len(doc_split) > 1:
            setattr(fn, '_long_help', doc_split[1])
        else:
            setattr(fn, '_long_help', '')
        return fn
    return inner


def skill_level(new_level):
    '''
    Use to set the required skill level of a command:

        @command
        @skill_level('administrator')
        def do_rmrf(self, cmd, args):
            ...
    '''
    if isinstance(new_level, basestring):
        levels = {'operator': 0, 'administrator': 1, 'expert': 2}
        if new_level.lower() not in levels:
            raise ValueError("Unknown skill level: " + new_level)
        new_level = levels[new_level.lower()]

    def inner(fn):
        setattr(fn, '_skill_level', new_level)
        return fn
    return inner


def wait(fn):
    '''
    A command with this decorator will
    force the interactive shell to wait
    for the command to complete.

        @command
        @wait
        def do_bigop(self, cmd, args):
            ...
    '''
    setattr(fn, '_wait', True)
    return fn


def completer(cb):
    '''
    Use to set a tab completer for the command.
    The completer is called for the command, regardless
    of the number of arguments called so far
    '''
    def inner(fn):
        setattr(fn, '_completer', cb)
        return fn
    return inner


def completers(*fns):
    '''
    Use to set a list of positional tab completers for the command.
    Each completer gets as its argument the command line entered so far,
    and returns a list of possible completions.
    '''
    def completer(args):
        nargs = len(args) - 1
        if nargs == 0:
            return [args[0]]
        if nargs <= len(fns):
            return fns[nargs-1](args)
        return []

    def inner(fn):
        setattr(fn, '_completer', completer)
        return fn
    return inner


def completers_repeating(*fns):
    '''
    Like completers, but calls the last completer
    for any additional arguments
    '''
    def completer(args):
        nargs = len(args) - 1
        if nargs == 0:
            return [args[0]]
        if nargs <= len(fns):
            return fns[nargs-1](args)
        return fns[-1](args)

    def inner(fn):
        setattr(fn, '_completer', completer)
        return fn
    return inner


def _cd_completer(args, context):
    'TODO: make better completion'
    ret = []
    if context.previous_level():
        ret += ['..']
    return ret + [l for l in context.current_level().get_completions()
                  if context.current_level().is_sublevel(l)]


def _help_completer(args, context):
    'TODO: make better completion'
    return help_module.list_help_topics() + context.current_level().get_completions()


def fuzzy_get(items, s):
    """
    Finds s in items using a fuzzy
    matching algorithm:

    1. if exact match, return value
    2. if unique prefix, return value
    3. if unique prefix substring, return value
    """
    found = items.get(s)
    if found:
        return found
    import re

    def fuzzy_match(rx):
        matcher = re.compile(rx, re.I)
        matches = [c
                   for m, c in items.iteritems()
                   if matcher.match(m)]
        if len(matches) == 1:
            return matches[0]
        return None

    # prefix match
    m = fuzzy_match(s + '.*')
    if m:
        return m
    # substring match
    m = fuzzy_match('.*'.join(s) + '.*')
    if m:
        return m
    return None


class UI(object):
    '''
    Base class for all ui levels.
    Things that I need to solve:
      - Error handling
      - Help
      - Completion
    '''

    # Name of level: override this in the subclass.
    name = None

    def requires(self):
        '''
        Returns False if requirements for level are
        not met. Checked before entering the level.
        '''
        return True

    def end_game(self, no_questions_asked=False):
        '''
        Overriding end_game() allows levels to ask
        for confirmation before exiting.
        '''
        pass

    def should_wait(self):
        '''
        A kludge to allow in-transit configuration changes to
        make us wait on transition to finish. Needs to be
        implemented in the level (currently, just configure).
        '''
        return False

    @alias('end', 'back')
    @help('''Go back to previous level
Navigates back in the user interface.
''')
    def do_up(self, context):
        '''
        TODO: Implement full cd navigation. cd ../configure, for example
        Also implement ls to list commands / levels from current location
        '''
        ok = context.up()
        context.save_stack()
        return ok

    @help('''List levels and commands
Lists the available sublevels and commands
at the current level.
''')
    def do_ls(self, context):
        '''
        Shows list of places to go and commands to call
        '''
        out = []
        if context.previous_level():
            out = ['..']
        out += context.current_level().get_completions()
        for i, o in enumerate(out):
            print '%-16s' % (o),
            if ((i - 2) % 3) == 0:
                print ''
        print ''

    @help('''Navigate the level structure
This command works similar to how `cd` works in a regular unix
system shell. `cd ..` returns to the previous level.

If the current level is `resource`, executing `cd ../configure` will
move directly to the `configure` level.

One difference between this command and the usual behavior of `cd`
is that without any argument, this command will go back one level
instead of doing nothing.

Examples:
....
        cd ..
        cd configure
        cd ../configure
        cd configure/ra
....
''')
    @completer(_cd_completer)
    def do_cd(self, context, optarg='..'):
        ok = True
        path = optarg.split('/', 1)
        if len(path) == 1:
            path = path[0]
            if path == '..':
                ok = context.up()
            elif path == '.' or not path:
                return ok
            else:
                info = context.current_level().get_child(path)
                if not info or not info.level:
                    common_debug("children: %s" % (self._children))
                    context.fatal_error("%s not found in %s" % (path, context.current_level()))
                context.enter_level(info.level)
        else:
            if not self.do_cd(context, path[0]):
                ok = False
            if not self.do_cd(context, path[1]):
                ok = False
        context.save_stack()
        return True

    @alias('bye', 'exit')
    @help('''Exit the interactive shell
Terminates `crm` immediately. For some levels, `quit` may
ask for confirmation before terminating, if there are
uncommitted changes to the configuration.
''')
    def do_quit(self, context):
        context.quit()

    @alias('?', '-h', '--help')
    @help('''show help (help topics for list of topics)
The help subsystem consists of the command reference and a list
of topics. The former is what you need in order to get the
details regarding a specific command. The latter should help with
concepts and examples.

Examples:
....
        help Introduction
        help quit
....
''')
    @completer(_help_completer)
    def do_help(self, context, subject=None, subtopic=None):
        """usage: help topic|level|command"""
        h = help_module.help_contextual(context.level_name(), subject, subtopic)
        h.paginate()

    def get_completions(self):
        '''
        return tab completions
        '''
        return self._children.keys()

    def get_child(self, child):
        '''
        Returns child info for the given name, or None
        if the child is not found.

        This tries very hard to find a matching child:
        If none is found, a fuzzy matcher is used to
        pick a close match
        '''
        return fuzzy_get(self._children, child)

    def is_sublevel(self, child):
        '''
        True if the given name is a sublevel of this level
        '''
        sub = self.get_child(child)
        return sub and sub.type == 'level'

    @classmethod
    def init_ui(cls):
        def get_if_command(attr):
            "Return the named attribute if it's a command"
            child = getattr(cls, attr)
            return child if attr.startswith('do_') and inspect.ismethod(child) else None

        def add_aliases(children, info):
            "Add any aliases for command to child map"
            for alias in info.aliases:
                children[alias] = info

        def add_help(info):
            "Add static help to the help system"
            if info.short_help:
                entry = help_module.HelpEntry(info.short_help, info.long_help, generated=True)
            elif info.type == 'command':
                entry = help_module.HelpEntry(
                    'Help for command ' + info.name,
                    'Note: This command is not documented.\n' +
                    'Usage: %s %s' % (info.name,
                                      ui_utils.pretty_arguments(info.function, nskip=2)),
                    generated=True)
            elif info.type == 'level':
                entry = help_module.HelpEntry('Help for level ' + info.name,
                                              'Note: This level is not documented.\n',
                                              generated=True)
            if info.type == 'command':
                help_module.add_help(entry, level=cls.name, command=info.name)
            elif info.type == 'level':
                help_module.add_help(entry, level=info.name)

        def prepare(children, child):
            info = ChildInfo(child, cls)
            if info.type == 'command' and not is_valid_command_function(info.function):
                raise ValueError("Invalid command function: %s.%s" %
                                 (cls.__name__, info.function.__name__))
            children[info.name] = info
            add_aliases(children, info)
            add_help(info)

        children = {}
        for child_name in dir(cls):
            child = get_if_command(child_name)
            if child:
                prepare(children, child)
        setattr(cls, '_children', children)
        return children


def make_name(new_name):
    '''
    Generate command name from command function name.
    '''
    if new_name.startswith('do_'):
        return new_name[3:]
    return new_name


class ChildInfo(object):
    '''
    Declares the given method a command method.
    Sets extra attributes in the function itself,
    which are picked up by the UILevel class and used
    to generate ChildInfo data.

    The given method is expected to take a first parameter
    (after self) which is a UI context, which holds information
    about where the user came from when calling the command, controls
    for manipulating the current level (up(), quit(), etc),
    the name used when calling the command, error reporting and warning
    methods.

    The rest of the parameters are the actual arguments to the method. These
    are tokenized using shlex and then matched to the actual arguments of the
    method.

    Information about a child node in the hierarchy:
    A node is either a level or a command.
    '''
    def __init__(self, fn, parent):
        def maybe(attr, default):
            if hasattr(fn, attr):
                return getattr(fn, attr)
            return default

        self.function = fn
        self.name = maybe('_name', make_name(fn.__name__))
        self.type = maybe('_ui_type', 'command')
        self.aliases = maybe('_aliases', tuple())
        self.short_help = maybe('_short_help', None)
        self.long_help = maybe('_long_help', None)
        self.skill_level = maybe('_skill_level', 0)
        self.wait = maybe('_wait', False)
        self.level = maybe('_level', None)
        self.completer = maybe('_completer', None)
        self.parent = parent
        self.children = {}
        if self.type == 'level' and self.level:
            self.children = self.level.init_ui()

    def complete(self, context, args):
        '''
        Execute the completer for this command with the given arguments.
        The completer mostly completes based on argument position, but
        some commands are context sensitive...
        - make args[0] be name of command
        '''
        ret = []
        if self.completer is not None:
            specs = inspect.getargspec(self.completer)
            if 'context' in specs.args:
                ret = self.completer([self.name] + args, context)
            else:
                ret = self.completer([self.name] + args)
        return ret

    def __repr__(self):
        return "%s:%s (%s)" % (self.type, self.name, self.short_help)


def is_valid_command_function(fn):
    '''
    Returns True if fn is a valid command function:
    named do_xxx, takes (self, context) as the first two parameters
    '''
    specs = inspect.getargspec(fn)
    return len(specs.args) >= 2 and specs.args[0] == 'self' and specs.args[1] == 'context'


def _check_args(fn, expected):
    argnames = fn.func_code.co_varnames[:fn.func_code.co_argcount]
    if argnames != expected:
        raise ValueError(fn.__name__ +
                         ": Expected method with signature " + repr(expected))
