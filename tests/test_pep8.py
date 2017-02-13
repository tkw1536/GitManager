import os
import unittest

import pep8

root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
ignore_patterns = ('env', '.git', '__pycache__')


def _ignore(directory: str) -> bool:
    """Should the directory be ignored?"""

    for pattern in ignore_patterns:
        if pattern in directory:
            return True
    return False


class SanityTest(unittest.TestCase):
    """Run PEP8 on all files in this directory and subdirectories."""

    def test_pep8_compliance(self):
        style = pep8.StyleGuide(quiet=False)
        errors = 0
        for root, _, files in os.walk(root_path):
            if _ignore(root):
                continue
            python_files = [os.path.join(root, f) for f in files if
                            f.endswith('.py')]
            errors += style.check_files(python_files).total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: {}'.format(errors))
