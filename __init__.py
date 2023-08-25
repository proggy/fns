#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2014-2023 Daniel Jung
# Contact: proggy-contact@mailbox.org
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""Tools for renaming files and folders to match my preferred file naming
scheme."""
__version__ = 'v0.1.0'

import os
import glob
import sys
import string


BADCHARS = ' _.,:;()[]{}"\'`~!?@#$%^&*=+/\\|<>'  # will be replaced by a dash

def dashify(files, test=False, verbose=False, alldots=False, nolower=False):
    """Rename the given list of files by replacing certain characters by
    dashes.

    Also does the following on the selected filenames:

        - All characters are switched to lowercase unless *nolower* is *True*.
        - The last dot in the filename is preserved unless *alldots* is *True*.
        - Adjacent dashes are reduced to only one dash.
        - Trailing dashes are removed.
        - Dashes in front of the suffix (last dot) are removed.
        - Leading dashes are removed.
        - Dashes separating characters followed by a digit are removed.

    It is possible to use filename patterns using the usual wildcard
    characters, e.g. "*" and "?".
    """

    # evaluate filename patterns, collect all filenames
    filenames = set()
    for filepattern in files:
        filepattern = os.path.expanduser(filepattern)
        results = glob.glob(filepattern)
        if not results:
            print(f'dashify: {filepattern}: no such file or directory', file=sys.stderr)
            sys.exit(1)
        for result in results:
            filenames.add(result)
    filenames = list(filenames)
    filenames.sort()

    # replace characters in filename
    for filename in filenames:
        newname = filename

        # switch to lowercase
        if not nolower:
            newname = newname.lower()

        for char in BADCHARS:
            if char == '.' and not alldots:
                dotcount = newname.count('.')
                newname = newname.replace(char, '-', dotcount-1)
            else:
                newname = newname.replace(char, '-')

        # contract adjacent dashes
        while '--' in newname:
            newname = newname.replace('--', '-')

        # remove trailing dash
        while newname and newname[-1] == '-':
            newname = newname[:-1]
        if '.' in newname:
            dotindex = newname.index('.')
            withoutsuffix = newname[:dotindex]
            suffix = newname[dotindex:]
            while withoutsuffix and withoutsuffix[-1] == '-':
                withoutsuffix = withoutsuffix[:-1]
            newname = withoutsuffix + suffix

        # remove leading dashes
        dirname, basename = os.path.dirname(newname), os.path.basename(newname)
        while basename[0] == '-':
            basename = basename[1:]
        newname = os.path.join(dirname, basename)

        # removed dashes that separate a character followed by a number
        index = 0
        while index < len(newname):
            if newname[index] == '-':
                if index < 1:
                    continue
                if index >= len(newname) - 1:
                    continue
                if newname[index-1] in string.ascii_letters \
                        and newname[index+1] in string.digits:
                    newname = newname[:index] + newname[(index+1):]
            index += 1

        # renaming results in something dangerous?
        if not newname:
            print(f'dashify: error: {filename}: omitting empty newname', file=sys.stderr)
            continue
        if newname == '.':
            print(f'dashify: error: {filename}: omitting invalid newname', file=sys.stderr)
            continue
        if filename[0] != '.' and newname[0] == '.':
            print(f'dashify: warning: {newname}: new name features a leading dot', file=sys.stderr)

        # no renaming necessary?
        if newname == filename:
            continue

        if verbose or test:
            print(f'{filename} --> {newname}')
        if not test:
            os.rename(filename, newname)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
