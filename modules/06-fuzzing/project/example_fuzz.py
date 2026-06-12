"""Minimal Atheris harness with a planted bug — your first crash.

Run:
    pip install atheris
    python example_fuzz.py

The `parse` function below has an intentional bug. Once Atheris finds the crash,
take the sanitizer/traceback output and feed it to your crash-triage augmentation
(see the module README) to root-cause and dedup it.
"""

import sys

try:
    import atheris
except ImportError:  # pragma: no cover
    sys.exit("Install atheris first: pip install atheris")


def parse(data: bytes) -> int:
    # Planted bug: trusts a length prefix without bounds-checking.
    if not data:
        return 0
    length = data[0]
    body = data[1:]
    return body[length]  # IndexError when length >= len(body)


def test_one_input(data: bytes) -> None:
    try:
        parse(data)
    except IndexError:
        # Re-raise as the kind of crash a real fuzzer should surface.
        raise


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
