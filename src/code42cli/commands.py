import inspect

from code42cli import profile as cliprofile
from code42cli.args import get_auto_arg_configs
from code42cli.sdk_client import create_sdk


class DictObject(object):
    def __init__(self, _dict):
        self.__dict__ = _dict


class Command(object):
    """Represents a function that a CLI user can execute. Add a command to 
    `code42cli.main._load_top_commands` or as a subcommand of one those
    commands to make it available for use.

    Args:
        name (str or unicode): The name of the command. For example, in
            `code42 profile show`, "show" is the name, while "profile"
            is the name of the parent command.

        description (str or unicode): Descriptive text to be displayed when using -h.

        usage (str, optional): A usage example to be displayed when using -h.
        handler (function, optional): The function to be exectued when the command is run.

        arg_customizer (function, optional): A function accepting a single `ArgCollection`
            parameter that allows for editing the collection when `get_arg_configs` is run.

        subcommand_loader (function, optional): A function returning a list of all subcommands
            parented by this command.

        use_single_arg_obj (bool, optional): When True, causes all parameters sent to
            `__call__` to be consolidated in an object with attribute names dictated
            by the parameter names. That object is passed to `handler`'s `arg` parameter.
    """

    def __init__(
        self,
        name,
        description,
        usage=None,
        handler=None,
        arg_customizer=None,
        subcommand_loader=None,
        use_single_arg_obj=None,
    ):

        self._name = name
        self._description = description
        self._usage = usage
        self._handler = handler
        self._arg_customizer = arg_customizer
        self._subcommand_loader = subcommand_loader
        self._use_single_arg_obj = use_single_arg_obj
        self._subcommands = []

    def __call__(self, *args, **kwargs):
        """Passes the parsed argparse args to the handler, or
        shows the help of for this command if there is no handler
        (common in commands that are simply groups of subcommands).
        """
        if callable(self._handler):
            kvps = _get_arg_kvps(args[0], self._handler)
            if self._use_single_arg_obj:
                kvps = _kvps_to_obj(kvps)
            return self._handler(**kvps)
        help_func = kwargs.pop(u"help_func", None)
        if help_func:
            return help_func()

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def usage(self):
        return self._usage

    @property
    def subcommands(self):
        return self._subcommands

    def load_subcommands(self):
        if callable(self._subcommand_loader):
            self._subcommands = self._subcommand_loader()

    def get_arg_configs(self):
        """Returns a collection of argparse configurations based on
        the parameter names of `handler` and any user customizations."""
        arg_config_collection = get_auto_arg_configs(self._handler)
        if callable(self._arg_customizer):
            self._arg_customizer(arg_config_collection)

        return arg_config_collection.arg_configs


def _get_arg_kvps(parsed_args, handler):
    # transform parsed args from argparse into a dict
    kvps = dict(vars(parsed_args))
    kvps.pop(u"func", None)
    return _inject_params(kvps, handler)


def _inject_params(kvps, handler):
    """automatically populates parameters named "sdk" or "profile" with instances of the sdk
    and profile, respectively."""
    if _handler_has_arg(u"sdk", handler):
        profile_name = kvps.pop(u"profile", None)
        debug = kvps.pop(u"debug", None)

        profile = cliprofile.get_profile(profile_name)
        kvps[u"sdk"] = create_sdk(profile, debug)

        if _handler_has_arg(u"profile", handler):
            kvps[u"profile"] = profile
    return kvps


def _handler_has_arg(arg_name, handler):
    argspec = inspect.getargspec(handler)
    return arg_name in argspec.args


def _kvps_to_obj(kvps):
    new_kvps = {key: kvps[key] for key in kvps if key in [u"sdk", u"profile"]}
    new_kvps[u"args"] = DictObject(kvps)
    return new_kvps