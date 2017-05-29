# agrep - Archive Grep

## Setup
```
pip install -r requirements.txt
```

## Usage
~~~
usage: agrep.py [--version] [--help] [-i] [-v] [-c] [--color] [-q] [-H] [-h]
                [-A NUM] [-B NUM] [-C NUM] [--exclude GLOB] [--include GLOB]
                PATTERN ARCHIVE [ARCHIVE ...]

positional arguments:
  PATTERN               Match pattern
  ARCHIVE               Target archive files

optional arguments:
  --version             show program's version number and exit
  --help

Matching Control:
  -i, --ignore-case     Ignore case distinctions in both the PATTERN and the
                        input files.
  -v, --invert-match    Invert the sense of matching, to select non-matching
                        lines.

General Output Control:
  -c, --count           Suppress normal output; instead print a count of
                        matching lines for each input file. With the -v,
                        --invert-match option (see below), count non-matching
                        lines.
  --color               Surround the matched (non-empty) strings, matching
                        lines, context lines, file names, line numbers, byte
                        offsets, and separators (for fields and groups of
                        context lines) with escape sequences to display them
                        in color on the terminal.
  -q, --quiet           Quiet; do not write anything to standard output. Exit
                        immediately with zero status if any match is found,
                        even if an error was detected.

Output Line Prefix Control:
  -H, --with-filename   Print the file name for each match. This is the
                        default.
  -h, --no-filename     Suppress the prefixing of file names on output.

Context Line Control:
  -A NUM, --after-context NUM
                        Print NUM lines of trailing context after matching
                        lines. Places a line containing a group separator (--)
                        between contiguous groups of matches.
  -B NUM, --before-context NUM
                        Print NUM lines of leading context before matching
                        lines. Places a line containing a group separator (--)
                        between contiguous groups of matches.
  -C NUM, --context NUM
                        Print NUM lines of output context. Places a line
                        containing a group separator (--) between contiguous
                        groups of matches.

File and Directory Selection:
  --exclude GLOB        Skip files whose base name matches GLOB (using
                        wildcard matching).
  --include GLOB        Search only files whose base name matches GLOB
~~~

