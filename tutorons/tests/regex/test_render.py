#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from django.test import Client
from bs4 import BeautifulSoup

from tutorons.regex.render import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestRenderRegexDescription(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.svg = "<svg class='my-svg'></svg>"
        self.example = "example"

    def test_introduction_appears(self):
        html = render(self.svg, self.example)
        doc = BeautifulSoup(html)
        self.assertIn("You found a regular expression", doc.text)

    def test_svg_included_in_description(self):
        html = render(self.svg, self.example)
        doc = BeautifulSoup(html)
        self.assertEqual(len(doc.select('svg')), 1)

    def test_description_include_example(self):
        html = render(self.svg, self.example)
        doc = BeautifulSoup(html)
        self.assertIn('This pattern can match a string like: example', doc.text)
