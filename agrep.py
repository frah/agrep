# -*- coding: utf-8 -*-
"""
agrep - Archive Grep
"""

__version__ = '0.0.0'

import re
import sys
import argparse
import chardet
import fnmatch
from zipfile import ZipFile
from colorama import init, Fore

class PatternAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            flags = 0
            if namespace.opt_ic:
                flags = re.IGNORECASE
            compiled_pattern = re.compile(values, flags=flags)
        except Exception:
            raise argparse.ArgumentError(self, 'Invalid pattern string')
        setattr(namespace, self.dest, compiled_pattern)
class ContextAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prev_context = getattr(namespace, self.dest)
        if option_string == '-A' or option_string == '--after-context':
            setattr(namespace, self.dest, (prev_context[0], values))
        elif option_string == '-B' or option_string == '--before-context':
            setattr(namespace, self.dest, (values, prev_context[1]))
        else:
            setattr(namespace, self.dest, (values, values))


def detect_enc(zfo, fname):
    with zfo.open(fname) as f:
        sample = f.read(10240)
        enc = chardet.detect(sample)
    return enc['encoding']

def do_grep(zf, zfo, fname, enc, args):
    if args.opt_out_fname:
        print_format = '{zip_name}/{file_name}:{line_number}:{text}'
    else:
        print_format = '{text}'

    with zfo.open(fname) as f:
        line_number = 0
        for line in f:
            line_number += 1
            line = line.decode(enc, errors='replace').strip()
            line = grep_format(line, args)
            if line:
                print(print_format.format(zip_name=zf, file_name=fname, line_number=line_number, text=line))

def grep_format(line, args):
    reg = args.pattern
    m = reg.search(line)
    if m is None:
        if args.opt_inv:
            return line
        else:
            return None

    if args.opt_color:
        sp = m.span()
        return line[:sp[0]] + Fore.RED + line[sp[0]:sp[1]] + Fore.RESET + line[sp[1]:]
    else:
        return line

def zip_grep(zf, zfo, args):
    flist = zfo.namelist()
    if args.opt_file_include is not None:
        flist = [fnmatch.filter(flist, g) for g in args.opt_file_include]
        flist = [flatten for inner in flist for flatten in inner]
    if args.opt_file_exclude is not None:
        elist = [fnmatch.filter(flist, g) for g in args.opt_file_exclude]
        elist = [flatten for inner in elist for flatten in inner]
        flist = [f for f in flist if f not in elist]
    for fname in flist:
        enc = detect_enc(zfo, fname)
        if enc is None:
            print("'{0}' is probably binary file. Skiped.".format(fname), file=sys.stderr)
            continue
        do_grep(zf, zfo, fname, enc, args)

def agrep(args):
    for zf in args.files:
        with ZipFile(zf) as zfo:
            zip_grep(zf, zfo, args)

if __name__ == '__main__':
    init()
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('pattern',
                   action=PatternAction, metavar='PATTERN',
                   help='Match pattern')
    p.add_argument('files', metavar='ARCHIVE', nargs='+',
                   help='Target archive files')
    p.add_argument('--version', action='version', version=__version__)
    p.add_argument('--help', action='help')

    g1 = p.add_argument_group('Matching Control')
    g1.add_argument('-i', '--ignore-case',
                 action='store_true', dest='opt_ic', default=False,
                 help='Ignore case distinctions in both the PATTERN and the input files.')
    g1.add_argument('-v', '--invert-match',
                 action='store_true', dest='opt_inv', default=False,
                 help='Invert the sense of matching, to select non-matching lines.')

    g2 = p.add_argument_group('General Output Control')
    g2.add_argument('-c', '--count',
                  action='store_true', dest='opt_cnt', default=False,
                  help='Suppress normal output; instead print a count of matching lines for each input file. With the -v, --invert-match option (see below), count non-matching lines.')
    g2.add_argument('--color',
                 action='store_true', dest='opt_color', default=False,
                 help='Surround the matched (non-empty) strings, matching lines, context lines, file names, line numbers, byte offsets, and separators (for fields and groups of context lines) with escape sequences to display them in color on the terminal.')
    g2.add_argument('-q', '--quiet',
                  action='store_true', dest='opt_q', default=False,
                  help='Quiet; do not write anything to standard output. Exit immediately with zero status if any match is found, even if an error was detected.')

    g3 = p.add_argument_group('Output Line Prefix Control')
    g3.add_argument('-H', '--with-filename',
                  action='store_true', dest='opt_out_fname', default=True,
                  help='Print the file name for each match. This is the default.')
    g3.add_argument('-h', '--no-filename',
                  action='store_false', dest='opt_out_fname', default=True,
                  help='Suppress the prefixing of file names on output.')

    g4 = p.add_argument_group('Context Line Control')
    g4.add_argument('-A', '--after-context',
                  action=ContextAction, dest='opt_context', type=int, metavar='NUM', default=(0, 0),
                  help='Print NUM lines of trailing context after matching lines. Places a line containing a group separator (--) between contiguous groups of matches.')
    g4.add_argument('-B', '--before-context',
                  action=ContextAction, dest='opt_context', type=int, metavar='NUM', default=(0, 0),
                  help='Print NUM lines of leading context before matching lines. Places a line containing a group separator (--) between contiguous groups of matches.')
    g4.add_argument('-C', '--context',
                  action=ContextAction, dest='opt_context', type=int, metavar='NUM', default=(0, 0),
                  help='Print NUM lines of output context. Places a line containing a group separator (--) between contiguous groups of matches.')

    g5 = p.add_argument_group('File and Directory Selection')
    g5.add_argument('--exclude',
                  action='append', dest='opt_file_exclude', metavar='GLOB',
                  help='Skip files whose base name matches GLOB (using wildcard matching).')
    g5.add_argument('--include',
                  action='append', dest='opt_file_include', metavar='GLOB',
                  help='Search only files whose base name matches GLOB')

    args = p.parse_args()
    print(args)
    agrep(args)
