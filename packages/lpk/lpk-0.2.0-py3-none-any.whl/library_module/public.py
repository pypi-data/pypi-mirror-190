def public_hello() -> None:
    print("hello")


def _file_private_hello() -> None:
    print("hello")


class PublicClass:
    """
    this is a public class
    """

    def __init__(self) -> None:
        ...

    ...

    @staticmethod
    def _static_protected_method() -> None:
        ...

    def public_method(self) -> None:
        ...

    def _protected_method(self) -> None:
        ...

    def __private_method(self) -> None:
        ...


class _FilePrivateClass:
    def __init__(self) -> None:
        ...


class public_namespace:
    # class

    a = 1

    class Public:
        ...

    class _NamespacePrivate:
        ...

    @staticmethod
    def hello() -> None:
        ...
