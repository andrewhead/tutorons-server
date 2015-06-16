#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import subprocess
import logging
import re
import os.path
from django.conf import settings

from tutorons.common.extractor import CommandExtractor
from tutorons.common.util import log_region
from parse_phrase import get_root_type, RootType
from opthelp import OPTHELP, COMBOHELP


logging.basicConfig(level=logging.INFO, format="%(message)s")
WGET = os.path.join(settings.DEPS_DIR, "wget", "src", "wget")
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


class WgetExtractor(object):

    def __init__(self):
        self.cmd_extractor = CommandExtractor(WGET_PATT)

    def extract(self, node):
        regions = self.cmd_extractor.extract(node)
        valid_regions = [r for r in regions if self._try_run(r.string)]
        [log_region(r) for r in valid_regions]
        return valid_regions

    def _try_run(self, wget_cmd):
        optstring = re.sub('^.*?' + WGET_PATT, '', wget_cmd)
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
            m = re.match("^LN: (.*)\|\|Value: (.*)\|\|SN: (.*)\|\|$", l)
            lname = r'--' + m.group(1) if m.group(1) != 'no' else None
            value = m.group(2) if m.group(2) != "null" else None
            sname = (r'-' + m.group(3)) if m.group(3) != '\x00' else ''
            if lname is None and sname is not None:
                lname = [ln for sn, ln, _ in OPTHELP if sn == sname][0]
            elif lname is None and sname is None:
                continue
            opts.append(Option(sname, lname, value))
        elif l.startswith("URL"):
            urlstr = re.sub('^URL: ', '', l)
            url = urlstr if urlstr != '(null)' else None

    return url, opts


''' Subroutines for parsing options. '''
_is_valued = lambda longname: True if '=' in longname else False
_get_value_name = lambda longname: longname.split('=')[1]


def build_help(longname=None, value=None, shortname=None):

    def _get_opt_by_longname(longname):
        for opt in OPTHELP:
            _, help_longname, msg = opt
            tok = help_longname.split('=')
            if tok[0] == longname:
                return opt
        return None

    def _get_opt_by_shortname(shortname):
        for opt in OPTHELP:
            help_shortname, _, msg = opt
            if help_shortname == shortname:
                return opt
        return None

    ''' Get an adaptive help message for an argument. '''
    if longname is not None:
        opt = _get_opt_by_longname(longname)
    elif shortname is not None:
        opt = _get_opt_by_shortname(shortname)
    else:
        return None

    if opt is None:
        return "No help found"

    _, help_longname, msg = opt
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="explain wget command line")
    parser.add_argument('cmd', help='wget command line to explain')
    args = parser.parse_args()
    exp = explain(args.cmd)
    print exp
