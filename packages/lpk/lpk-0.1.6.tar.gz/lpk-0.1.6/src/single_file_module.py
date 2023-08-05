# this can be both binary and library.
# as library module when imported from other files.
# as binary module when executed directly.


def can_be_imported() -> None:
    print("imported")


def _run_as_binary() -> None:
    print("run as binary")


if __name__ == "__main__":
    _run_as_binary()
