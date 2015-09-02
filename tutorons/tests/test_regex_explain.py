#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import httpretty
from django.conf import settings

from tutorons.regex.explain import InvalidRegexException, visualize as regex_viz


logging.basicConfig(level=logging.INFO, format="%(message)s")


class RegexVisualizeFailureTest(unittest.TestCase):

    @httpretty.activate
    def test_dont_throw_excpetion_on_valid_svg(self):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg><g class='root'></g></svg></div></div>")
        regex_viz('test-pattern')

    @httpretty.activate
    def test_throw_exception_when_regexper_svg_has_no_root(self):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg></svg></div></div>")
        with self.assertRaises(InvalidRegexException):
            regex_viz('test-pattern')
