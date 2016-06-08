# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\17I\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6")
        buf.write(u"\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\13\6\13\63")
        buf.write(u"\n\13\r\13\16\13\64\3\f\5\f8\n\f\3\f\3\f\6\f<\n\f\r\f")
        buf.write(u"\16\f=\3\f\5\fA\n\f\3\r\3\r\3\16\6\16F\n\16\r\16\16\16")
        buf.write(u"G\2\2\17\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write(u"\f\27\r\31\16\33\17\3\2\4\7\2//\62;C\\aac|\3\2\"\"N\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2")
        buf.write(u"\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write(u"\2\2\3\35\3\2\2\2\5\37\3\2\2\2\7!\3\2\2\2\t#\3\2\2\2")
        buf.write(u"\13%\3\2\2\2\r(\3\2\2\2\17*\3\2\2\2\21,\3\2\2\2\23.\3")
        buf.write(u"\2\2\2\25\62\3\2\2\2\27\67\3\2\2\2\31B\3\2\2\2\33E\3")
        buf.write(u"\2\2\2\35\36\7\f\2\2\36\4\3\2\2\2\37 \7\60\2\2 \6\3\2")
        buf.write(u"\2\2!\"\7%\2\2\"\b\3\2\2\2#$\7<\2\2$\n\3\2\2\2%&\7<\2")
        buf.write(u"\2&\'\7<\2\2\'\f\3\2\2\2()\7]\2\2)\16\3\2\2\2*+\7_\2")
        buf.write(u"\2+\20\3\2\2\2,-\7?\2\2-\22\3\2\2\2./\7`\2\2/\60\7?\2")
        buf.write(u"\2\60\24\3\2\2\2\61\63\5\31\r\2\62\61\3\2\2\2\63\64\3")
        buf.write(u"\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2\65\26\3\2\2\2\668")
        buf.write(u"\7)\2\2\67\66\3\2\2\2\678\3\2\2\28;\3\2\2\29<\5\31\r")
        buf.write(u"\2:<\7\61\2\2;9\3\2\2\2;:\3\2\2\2<=\3\2\2\2=;\3\2\2\2")
        buf.write(u"=>\3\2\2\2>@\3\2\2\2?A\7)\2\2@?\3\2\2\2@A\3\2\2\2A\30")
        buf.write(u"\3\2\2\2BC\t\2\2\2C\32\3\2\2\2DF\t\3\2\2ED\3\2\2\2FG")
        buf.write(u"\3\2\2\2GE\3\2\2\2GH\3\2\2\2H\34\3\2\2\2\t\2\64\67;=")
        buf.write(u"@G\2")
        return buf.getvalue()


class CssLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    IDENT = 10
    VALUE = 11
    IDCHAR = 12
    SPACE = 13

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'\n'", u"'.'", u"'#'", u"':'", u"'::'", u"'['", u"']'", u"'='", 
            u"'^='" ]

    symbolicNames = [ u"<INVALID>",
            u"IDENT", u"VALUE", u"IDCHAR", u"SPACE" ]

    ruleNames = [ u"T__0", u"T__1", u"T__2", u"T__3", u"T__4", u"T__5", 
                  u"T__6", u"T__7", u"T__8", u"IDENT", u"VALUE", u"IDCHAR", 
                  u"SPACE" ]

    grammarFileName = u"Css.g4"

    def __init__(self, input=None):
        super(CssLexer, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


