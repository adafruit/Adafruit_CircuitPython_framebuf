# SPDX-FileCopyrightText: 2026 Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Check that every method and function in adafruit_framebuf has type annotations."""

import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import adafruit_framebuf  # noqa: E402


def _unwrap(attr):
    """Return the plain functions behind a class attribute."""
    if isinstance(attr, (staticmethod, classmethod)):
        return [attr.__func__]
    if isinstance(attr, property):
        return [f for f in (attr.fget, attr.fset) if f is not None]
    if inspect.isfunction(attr):
        return [attr]
    return []


class TypeAnnotationTest(unittest.TestCase):
    """Every public function and method should be annotated."""

    def test_all_functions_annotated(self):
        missing = []
        for cls_name, cls in vars(adafruit_framebuf).items():
            if not inspect.isclass(cls) or cls.__module__ != adafruit_framebuf.__name__:
                continue
            for name, attr in vars(cls).items():
                for func in _unwrap(attr):
                    sig = inspect.signature(func)
                    unannotated = [
                        p for p in sig.parameters.values()
                        if p.name != "self" and p.annotation is inspect.Parameter.empty
                    ]
                    if sig.return_annotation is inspect.Signature.empty or unannotated:
                        missing.append(f"{cls_name}.{name}")
        self.assertFalse(missing, "missing annotations: " + ", ".join(sorted(set(missing))))


if __name__ == "__main__":
    unittest.main()
