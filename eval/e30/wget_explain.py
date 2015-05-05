#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import subprocess
import logging
import jsonpickle
import json
import re
import os.path
import sys

from parse_phrase import get_root_type, RootType
from opthelp import OPTHELP, COMBOHELP


logging.basicConfig(level=logging.INFO, format="%(message)s")
WGET = os.path.join("wget-1.16", "src", "wget")
PREAMBLE = "wget is a Terminal command you run to download a page from the Internet."
URL_LINE = "This command downloads the page at {url}."


class Option(object):

    def __init__(self, short_name, long_name, value):
        self.short_name = short_name
        self.long_name = long_name
        self.value = value

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


def explain(cmd):

    explanation = PREAMBLE
    optstring = re.sub('.*?wget(?:.exe)?', '', cmd)
    url, opts = parse_options(optstring)

    if url is not None:
        explanation += " " + URL_LINE.format(url=url)
    explanation += '\n'

    combo_exps = optcombo_explain(url, opts)
    for ce in combo_exps:
        explanation += ce + '\n'

    for opt in opts:
        opthelp = build_help(opt.long_name, opt.value)
        templ = "{ln}"
        templ = (templ + " ({sn})") if opt.short_name else templ
        templ += ": {opthelp}\n"
        optexp = templ.format(ln=opt.long_name, sn=opt.short_name, opthelp=opthelp)
        explanation += optexp

    return explanation


def optcombo_explain(url, options):

    optnames = [opt.long_name for opt in options]
    explanations = []
    templ_args = {'url': url}
    for opt in options:
        key = re.sub('^--', '', opt.long_name)
        templ_args[key] = opt.value

    for optcombo, templ in COMBOHELP.items():
        match = all([opt in optnames for opt in optcombo])
        if match:
            exp = templ.format(**templ_args)
            explanations.append(exp)
            # Remove all explained options from the list of options that need
            # to be explained to avoid redundant explanations.
            [optnames.pop(optnames.index(opt)) for opt in optcombo]
        
    return explanations


def parse_options(optstring):

    cmd = str(WGET) + optstring
    stdout = subprocess.check_output(cmd.split(' '))
    lines = stdout.split("\n")
    opts = []
    url = None

    for l in lines:
        if l.startswith("LN"):
            m = re.match("^LN: (.*)\|\|SN: (.*)\|\|Type: (.*)\|\|Value: (.*)$", l)
            lname = r'--' + m.group(1)
            sname = (r'-' + m.group(2)) if m.group(2) != '\x00' else ''
            value = m.group(4) if m.group(4) != "null" else None
            opts.append(Option(sname, lname, value))
        elif l.startswith("URL"):
            urlstr = re.sub('^URL: ', '', l)
            url = urlstr if urlstr != '(null)' else None

    return url, opts


''' Subroutines for parsing options. '''
_is_valued = lambda longname: True if '=' in longname else False
_get_value_name = lambda longname: longname.split('=')[1]


def build_help(longname, value=None):
    ''' Get an adaptive help message for an argument. '''
    for _, help_longname, msg in OPTHELP:
        if help_longname.startswith(longname):
            if _is_valued(help_longname):
                vname = _get_value_name(help_longname)
                if vname in msg:
                    msg = msg.replace(vname, value)
                elif get_root_type(msg) == RootType.NOUN:
                    msg = value + " is a " + msg
                else:
                    appendix = " ({0}={1})".format(vname, value)
                    msg = re.sub("(.?)$", r"{0}\1".format(appendix), msg)
            return msg
    return "No help found"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="explain wget command line")
    parser.add_argument('cmd', help='wget command line to explain')
    args = parser.parse_args()
    exp = explain(args.cmd)
    print exp
