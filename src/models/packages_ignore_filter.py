from typing import Set, FrozenSet, Tuple, TypeAlias

from packageurl import PackageURL

from src.arguments.action_arguments import ActionArguments

# Tuple type representing package to ignore fo checking: `type`, `namespace` and `name`.
# The former two have supports dedicated asterisk symbol `*` that is considered as 'ignore all'.
# For instance, tuple `('maven', 'com.example', '*')` will be treated as ignore all packages for type 'maven' and
# namespace 'com.example'.
PackageIgnore: TypeAlias = Tuple[str, str, str]

ASTERISK = "*"


class PackagesIgnoreFilter:
    """
    Creates filter implementation to filter out packages for maintenance check based on
    `packages_ignore` action argument. Packages to ignore are identified as package URL, but only
    `type`, `name` and `namespace` are taken into account. `name` and `namespace` might have asterisk (`*`) value
    this is treated as 'ignore all'.
    For instance, tuple `('maven', 'com.example', '*')` will be treated as ignore all packages for type 'maven' and
    namespace 'com.example'.
    """

    @staticmethod
    def create(arguments: ActionArguments):
        """
        Create new filter from arguments

        :param arguments: action arguments to supplied to the action.
        :return: constructed filter.
        """
        ignore: Set[PackageIgnore] = set()
        if arguments.packages_ignore is not None:
            for package in arguments.packages_ignore:
                package_ignore: PackageIgnore = (
                    package.type,
                    package.namespace or ASTERISK,
                    package.name,
                )
                ignore.add(package_ignore)
        return PackagesIgnoreFilter(frozenset(ignore))

    def __init__(self, ignore: FrozenSet[PackageIgnore]):
        self._ignore = ignore

    def ignore(self, purl: PackageURL) -> bool:
        """
        Check whether to proceed with package or ignore it, based on `packages_ignore` action argument.

        :param purl: package URL to check
        :return: True if to ignore package, False if to check
        """
        ignore_all_type_item = (purl.type, ASTERISK, ASTERISK)
        ignore_all_namespaces_item = (purl.type, purl.namespace, ASTERISK)
        ignore_all_names_item = (purl.type, purl.namespace, purl.name)
        return (
            (ignore_all_type_item in self._ignore)
            | (ignore_all_namespaces_item in self._ignore)
            | (ignore_all_names_item in self._ignore)
        )
