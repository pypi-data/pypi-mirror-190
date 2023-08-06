#! /usr/bin/env python
"""Rez build file, must cd to this directory and run "rez build"."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from rez_builder import PipFromSrcBuilder

if __name__ == "__main__":
    BUILDER = PipFromSrcBuilder({})
    BUILDER.build()
