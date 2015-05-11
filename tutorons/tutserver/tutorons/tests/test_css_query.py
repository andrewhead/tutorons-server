#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestRenderDescription(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_resp_texts(self, payload):
        resp = self.client.post('/css', content_type='raw', data=payload)
        respData = json.loads(resp.content)
        texts = {k: BeautifulSoup(v).text for k,v in respData.items()}
        return texts

    def get_example_html(self, payload):
        resp = self.client.post('/css', content_type='raw', data=payload)
        respData = json.loads(resp.content)
        return respData

    def get_text_short(self, selector):
        return self.get_resp_texts('\n'.join(["<code>", selector, "</code>"]))

    def get_example_short(self, selector):
        return self.get_example_html('\n'.join(["<code>", selector, "</code>"]))

    def test_describe_preamble(self):
        texts = self.get_text_short('$(".klazz")')
        text = texts['.klazz']
        self.assertIn("You found a CSS selector", text)
        self.assertIn("selectors pick sections of HTML pages", text)

    def test_describe_single_class(self):
        texts = self.get_text_short('$(".watch-view-count")')
        self.assertEqual(len(texts.keys()), 1)
        text = texts['.watch-view-count']
        self.assertIn("chooses elements of class 'watch-view-count'", text)

    def test_render_example_html(self):
        doms = self.get_example_html('<code>$("div p");</code>')
        dom = doms['div p']
        self.assertIn("\n".join([
            "&lt;div&gt;<br>",
            "<span class='tutoron_selection'>",
            "&nbsp;&nbsp;&nbsp;&nbsp;&lt;p&gt;<br>",
            "&nbsp;&nbsp;&nbsp;&nbsp;&lt;/p&gt;<br>",
            "</span>",
            "&lt;/div&gt;<br>",
        ]), dom)
