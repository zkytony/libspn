# ------------------------------------------------------------------------
# Copyright (C) 2016-2017 Andrzej Pronobis - All Rights Reserved
#
# This file is part of LibSPN. Unauthorized use or copying of this file,
# via any medium is strictly prohibited. Proprietary and confidential.
# ------------------------------------------------------------------------

"""LibSPN documentation utilities."""


class docinherit:

    """A decorator for inheriting docstrings from base classes."""

    def __init__(self, parent):
        self.parent = parent

    def __call__(self, fun):
        parent_fun = getattr(self.parent, fun.__name__, None)
        fun.__doc__ = parent_fun.__doc__
        return fun
