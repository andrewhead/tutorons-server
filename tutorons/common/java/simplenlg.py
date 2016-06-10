#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from py4j.java_gateway import java_import

from tutorons.common.java.gateway import gateway


logging.basicConfig(level=logging.INFO, format="%(message)s")


# Load all of the SimpleNLG dependencies we might want to access from Python code.
# The variables assigned below can be imported as if they were Python classes.
java_import(gateway.jvm, 'simplenlg.features.*')
java_import(gateway.jvm, 'simplenlg.realiser.english.*')
java_import(gateway.jvm, 'simplenlg.framework.*')
java_import(gateway.jvm, 'simplenlg.lexicon.*')

lexicon = gateway.jvm.Lexicon.getDefaultLexicon()
factory = gateway.jvm.NLGFactory(lexicon)
realiser = gateway.jvm.Realiser(lexicon)
NumberAgreement = gateway.jvm.NumberAgreement
Feature = gateway.jvm.Feature
