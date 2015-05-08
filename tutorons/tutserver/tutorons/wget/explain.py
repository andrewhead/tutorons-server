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
from django.conf import settings

from parse_phrase import get_root_type, RootType
from opthelp import OPTHELP, COMBOHELP


logging.basicConfig(level=logging.INFO, format="%(message)s")
WGET = os.path.join(settings.DEPS_DIR, "wget-1.16", "src", "wget")
WGET_PATT = r"wget(?:.exe)?"


class Option(object):

    def __init__(self, short_name, long_name, value):
        self.short_name = short_name
        self.long_name = long_name
        self.value = value
        self.help = ""

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


def detect(cmd):
    """ Detect whether this is a valid wget command line. """

    if len(cmd) == 0 or not re.match('^(.*?\W)?' + WGET_PATT, cmd):
        return False

    optstring = re.sub('^.*?' + WGET_PATT, '', cmd)
    cmd = str(WGET) + optstring
    try:
        subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    return True


def explain(cmd):
    """ Convert command line into objects that can be explained. """

    explanation = {}

    optstring = re.sub('^.*?' + WGET_PATT, '', cmd)
    url, opts = parse_options(optstring)
    explanation['url'] = url

    for opt in opts:
        opt.help = build_help(opt.long_name, opt.value)
    explanation['opts'] = opts

    combo_exps = optcombo_explain(url, opts)
    explanation['combo_exps'] = combo_exps

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
