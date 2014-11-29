#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from skim.parse import Concept, parseConcepts, getClass, parseClasses
import unittest


class ParseClassesTest(unittest.TestCase):

    def testGetObjectAfterConstructor(self):
        classes = parseClasses("ITrain train = null;")
        self.assertIn("ITrain", classes)

    def testGetClassnameFromDeclaration(self):
        classes = parseClasses("train = new Train(15);")
        self.assertIn("Train", classes)

    def testParseMultipleClasses(self):
        classes = parseClasses("ITrain train = new Train(15);")
        self.assertIn("ITrain", classes)
        self.assertIn("Train", classes)

    def testParseNestedNews(self):
        classes = parseClasses("ITrain train = new Train(new Steamer());")
        self.assertIn("ITrain", classes)
        self.assertIn("Train", classes)
        self.assertIn("Steamer", classes)


class FilterInlineCodeClassesTest(unittest.TestCase):
 
    def testMustStartWithCapital(self):
        self.assertIsNone(getClass('char[]'))

    def testNothingBeyondPeriod(self):
        self.assertEquals(getClass('MyClass.member.method'), 'MyClass')


class ParseArithOpsTest(unittest.TestCase):

    def testParsePlus(self):
        concepts = parseConcepts("a = b + c;")
        self.assertIn(Concept.ARITHMETIC_OP, concepts)

    def testParseMinus(self):
        concepts = parseConcepts("a = b - c;")
        self.assertIn(Concept.ARITHMETIC_OP, concepts)

    def testParseTimes(self):
        concepts = parseConcepts("a = b * c;")
        self.assertIn(Concept.ARITHMETIC_OP, concepts)

    def testParseSlash(self):
        concepts = parseConcepts("a = b / c;")
        self.assertIn(Concept.ARITHMETIC_OP, concepts)


class ParseRelOpsTest(unittest.TestCase):

    def testParseGreaterThan(self):
        concepts = parseConcepts("a = b > c;")
        self.assertIn(Concept.RELATIONAL_OP, concepts)

    def testParseLessThan(self):
        concepts = parseConcepts("a = b < c;")
        self.assertIn(Concept.RELATIONAL_OP, concepts)

    def testParseEquals(self):
        concepts = parseConcepts("a = b == c;")
        self.assertIn(Concept.RELATIONAL_OP, concepts)

    def testParseNotEquals(self):
        concepts = parseConcepts("a = b != c;")
        self.assertIn(Concept.RELATIONAL_OP, concepts)


class ParseMultipleTest(unittest.TestCase):

    def testParseRelOpAndArithOp(self):
        concepts = parseConcepts("a = (b > c + 5);")
        self.assertIn(Concept.RELATIONAL_OP, concepts)
        self.assertIn(Concept.ARITHMETIC_OP, concepts)


class ParseLoopsTest(unittest.TestCase):

    def testParseForLoop(self):
        concepts = parseConcepts("	for (int i = 0; i < 2; i++) {")
        self.assertIn(Concept.LOOP, concepts)

    def testParseForLoopAtStartOfLine(self):
        concepts = parseConcepts("for (int i = 0; i < 2; i++) {")
        self.assertIn(Concept.LOOP, concepts)

    def testParseForWithNoSpaceBeforeParens(self):
        concepts = parseConcepts("for(int i = 0; i < 2; i++) {")
        self.assertIn(Concept.LOOP, concepts)

    def testParseWhileLoop(self):
        concepts = parseConcepts("while(i > 0)")
        self.assertIn(Concept.LOOP, concepts)

    def testNoParseForLoopFromVarname(self):
        concepts = parseConcepts("format = 2;")
        self.assertNotIn(Concept.LOOP, concepts)


class ParseAssignmentTest(unittest.TestCase):

    def testParseAssignmentFromEquals(self):
        concepts = parseConcepts("a = 2;")
        self.assertIn(Concept.ASSIGNMENT, concepts)

    def testNoParseDoubleEqualsRelational(self):
        concepts = parseConcepts("if (a == 3) {")
        self.assertNotIn(Concept.ASSIGNMENT, concepts)


class ParseConditionalsTest(unittest.TestCase):

    def testParseIfStatement(self):
        concepts = parseConcepts("	if (i == 5) {")
        self.assertIn(Concept.CONDITIONAL, concepts)

    def testNoParseIfFromVarName(self):
        concepts = parseConcepts("int iffy = 5;");
        self.assertNotIn(Concept.CONDITIONAL, concepts)


class ParseReturnTest(unittest.TestCase):

    def testParseReturn(self):
        concepts = parseConcepts("return String();")
        self.assertIn(Concept.RETURN, concepts)


class ParseArraysTest(unittest.TestCase):

    def testParseLeftBracket(self):
        concepts = parseConcepts("int a = b[2];")
        self.assertIn(Concept.ARRAY, concepts)


class ParseObjectsTest(unittest.TestCase):

    def testParseNewStatement(self):
        concepts = parseConcepts("String b = new String();")
        self.assertIn(Concept.OBJECT, concepts)


class ParseFunctionTest(unittest.TestCase):

    def testFunctionDeclarationOpeningParenNoSemicolon(self):
        concepts = parseConcepts("public void helloWorld() ")
        self.assertIn(Concept.FUNCTION, concepts)
 
    def testNoFunctionIfNoPrivatePublicKeyword(self):
        concepts = parseConcepts("void helloWorld() ")
        self.assertNotIn(Concept.FUNCTION, concepts)

    def testNoFunctionIfEndsWithSemicolon(self):
        concepts = parseConcepts("helloWorld(1, 2);")
        self.assertNotIn(Concept.FUNCTION, concepts)
