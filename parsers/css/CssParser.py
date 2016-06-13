# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .CssListener import CssListener
else:
    from CssListener import CssListener
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\36\u00cd\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\2\7\2$\n\2")
        buf.write(u"\f\2\16\2\'\13\2\3\2\7\2*\n\2\f\2\16\2-\13\2\3\3\3\3")
        buf.write(u"\3\3\3\3\7\3\63\n\3\f\3\16\3\66\13\3\3\4\3\4\7\4:\n\4")
        buf.write(u"\f\4\16\4=\13\4\3\4\3\4\7\4A\n\4\f\4\16\4D\13\4\3\4\3")
        buf.write(u"\4\7\4H\n\4\f\4\16\4K\13\4\3\4\6\4N\n\4\r\4\16\4O\5\4")
        buf.write(u"R\n\4\3\5\3\5\5\5V\n\5\3\5\3\5\3\5\3\5\3\5\7\5]\n\5\f")
        buf.write(u"\5\16\5`\13\5\3\6\5\6c\n\6\3\6\3\6\3\7\5\7h\n\7\3\7\3")
        buf.write(u"\7\3\b\3\b\3\t\5\to\n\t\3\t\3\t\3\n\3\n\3\n\3\13\3\13")
        buf.write(u"\7\13x\n\13\f\13\16\13{\13\13\3\13\5\13~\n\13\3\13\3")
        buf.write(u"\13\7\13\u0082\n\13\f\13\16\13\u0085\13\13\3\13\3\13")
        buf.write(u"\7\13\u0089\n\13\f\13\16\13\u008c\13\13\3\13\3\13\7\13")
        buf.write(u"\u0090\n\13\f\13\16\13\u0093\13\13\5\13\u0095\n\13\3")
        buf.write(u"\13\3\13\3\f\3\f\5\f\u009b\n\f\3\f\3\f\5\f\u009f\n\f")
        buf.write(u"\3\r\3\r\7\r\u00a3\n\r\f\r\16\r\u00a6\13\r\3\r\3\r\3")
        buf.write(u"\r\3\16\3\16\7\16\u00ad\n\16\f\16\16\16\u00b0\13\16\6")
        buf.write(u"\16\u00b2\n\16\r\16\16\16\u00b3\3\17\3\17\7\17\u00b8")
        buf.write(u"\n\17\f\17\16\17\u00bb\13\17\3\17\3\17\7\17\u00bf\n\17")
        buf.write(u"\f\17\16\17\u00c2\13\17\3\17\3\17\3\20\3\20\3\20\3\20")
        buf.write(u"\3\20\5\20\u00cb\n\20\3\20\2\2\21\2\4\6\b\n\f\16\20\22")
        buf.write(u"\24\26\30\32\34\36\2\6\4\2\3\3\22\22\4\2\7\7\r\21\3\2")
        buf.write(u"\22\23\7\2\13\13\22\23\25\25\27\27\36\36\u00e1\2 \3\2")
        buf.write(u"\2\2\4.\3\2\2\2\6Q\3\2\2\2\bU\3\2\2\2\nb\3\2\2\2\fg\3")
        buf.write(u"\2\2\2\16k\3\2\2\2\20n\3\2\2\2\22r\3\2\2\2\24u\3\2\2")
        buf.write(u"\2\26\u0098\3\2\2\2\30\u00a0\3\2\2\2\32\u00b1\3\2\2\2")
        buf.write(u"\34\u00b5\3\2\2\2\36\u00ca\3\2\2\2 +\5\4\3\2!%\7\31\2")
        buf.write(u"\2\"$\7\f\2\2#\"\3\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3\2\2")
        buf.write(u"\2&(\3\2\2\2\'%\3\2\2\2(*\5\4\3\2)!\3\2\2\2*-\3\2\2\2")
        buf.write(u"+)\3\2\2\2+,\3\2\2\2,\3\3\2\2\2-+\3\2\2\2.\64\5\b\5\2")
        buf.write(u"/\60\5\6\4\2\60\61\5\b\5\2\61\63\3\2\2\2\62/\3\2\2\2")
        buf.write(u"\63\66\3\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2\65\5\3\2\2")
        buf.write(u"\2\66\64\3\2\2\2\67;\7\27\2\28:\7\f\2\298\3\2\2\2:=\3")
        buf.write(u"\2\2\2;9\3\2\2\2;<\3\2\2\2<R\3\2\2\2=;\3\2\2\2>B\7\30")
        buf.write(u"\2\2?A\7\f\2\2@?\3\2\2\2AD\3\2\2\2B@\3\2\2\2BC\3\2\2")
        buf.write(u"\2CR\3\2\2\2DB\3\2\2\2EI\7\32\2\2FH\7\f\2\2GF\3\2\2\2")
        buf.write(u"HK\3\2\2\2IG\3\2\2\2IJ\3\2\2\2JR\3\2\2\2KI\3\2\2\2LN")
        buf.write(u"\7\f\2\2ML\3\2\2\2NO\3\2\2\2OM\3\2\2\2OP\3\2\2\2PR\3")
        buf.write(u"\2\2\2Q\67\3\2\2\2Q>\3\2\2\2QE\3\2\2\2QM\3\2\2\2R\7\3")
        buf.write(u"\2\2\2SV\5\n\6\2TV\5\20\t\2US\3\2\2\2UT\3\2\2\2V^\3\2")
        buf.write(u"\2\2W]\7\26\2\2X]\5\22\n\2Y]\5\24\13\2Z]\5\26\f\2[]\5")
        buf.write(u"\34\17\2\\W\3\2\2\2\\X\3\2\2\2\\Y\3\2\2\2\\Z\3\2\2\2")
        buf.write(u"\\[\3\2\2\2]`\3\2\2\2^\\\3\2\2\2^_\3\2\2\2_\t\3\2\2\2")
        buf.write(u"`^\3\2\2\2ac\5\f\7\2ba\3\2\2\2bc\3\2\2\2cd\3\2\2\2de")
        buf.write(u"\5\16\b\2e\13\3\2\2\2fh\t\2\2\2gf\3\2\2\2gh\3\2\2\2h")
        buf.write(u"i\3\2\2\2ij\7\4\2\2j\r\3\2\2\2kl\7\22\2\2l\17\3\2\2\2")
        buf.write(u"mo\5\f\7\2nm\3\2\2\2no\3\2\2\2op\3\2\2\2pq\7\3\2\2q\21")
        buf.write(u"\3\2\2\2rs\7\5\2\2st\7\22\2\2t\23\3\2\2\2uy\7\6\2\2v")
        buf.write(u"x\7\f\2\2wv\3\2\2\2x{\3\2\2\2yw\3\2\2\2yz\3\2\2\2z}\3")
        buf.write(u"\2\2\2{y\3\2\2\2|~\5\f\7\2}|\3\2\2\2}~\3\2\2\2~\177\3")
        buf.write(u"\2\2\2\177\u0083\7\22\2\2\u0080\u0082\7\f\2\2\u0081\u0080")
        buf.write(u"\3\2\2\2\u0082\u0085\3\2\2\2\u0083\u0081\3\2\2\2\u0083")
        buf.write(u"\u0084\3\2\2\2\u0084\u0094\3\2\2\2\u0085\u0083\3\2\2")
        buf.write(u"\2\u0086\u008a\t\3\2\2\u0087\u0089\7\f\2\2\u0088\u0087")
        buf.write(u"\3\2\2\2\u0089\u008c\3\2\2\2\u008a\u0088\3\2\2\2\u008a")
        buf.write(u"\u008b\3\2\2\2\u008b\u008d\3\2\2\2\u008c\u008a\3\2\2")
        buf.write(u"\2\u008d\u0091\t\4\2\2\u008e\u0090\7\f\2\2\u008f\u008e")
        buf.write(u"\3\2\2\2\u0090\u0093\3\2\2\2\u0091\u008f\3\2\2\2\u0091")
        buf.write(u"\u0092\3\2\2\2\u0092\u0095\3\2\2\2\u0093\u0091\3\2\2")
        buf.write(u"\2\u0094\u0086\3\2\2\2\u0094\u0095\3\2\2\2\u0095\u0096")
        buf.write(u"\3\2\2\2\u0096\u0097\7\b\2\2\u0097\25\3\2\2\2\u0098\u009a")
        buf.write(u"\7\t\2\2\u0099\u009b\7\t\2\2\u009a\u0099\3\2\2\2\u009a")
        buf.write(u"\u009b\3\2\2\2\u009b\u009e\3\2\2\2\u009c\u009f\7\22\2")
        buf.write(u"\2\u009d\u009f\5\30\r\2\u009e\u009c\3\2\2\2\u009e\u009d")
        buf.write(u"\3\2\2\2\u009f\27\3\2\2\2\u00a0\u00a4\7\24\2\2\u00a1")
        buf.write(u"\u00a3\7\f\2\2\u00a2\u00a1\3\2\2\2\u00a3\u00a6\3\2\2")
        buf.write(u"\2\u00a4\u00a2\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5\u00a7")
        buf.write(u"\3\2\2\2\u00a6\u00a4\3\2\2\2\u00a7\u00a8\5\32\16\2\u00a8")
        buf.write(u"\u00a9\7\n\2\2\u00a9\31\3\2\2\2\u00aa\u00ae\t\5\2\2\u00ab")
        buf.write(u"\u00ad\7\f\2\2\u00ac\u00ab\3\2\2\2\u00ad\u00b0\3\2\2")
        buf.write(u"\2\u00ae\u00ac\3\2\2\2\u00ae\u00af\3\2\2\2\u00af\u00b2")
        buf.write(u"\3\2\2\2\u00b0\u00ae\3\2\2\2\u00b1\u00aa\3\2\2\2\u00b2")
        buf.write(u"\u00b3\3\2\2\2\u00b3\u00b1\3\2\2\2\u00b3\u00b4\3\2\2")
        buf.write(u"\2\u00b4\33\3\2\2\2\u00b5\u00b9\7\33\2\2\u00b6\u00b8")
        buf.write(u"\7\f\2\2\u00b7\u00b6\3\2\2\2\u00b8\u00bb\3\2\2\2\u00b9")
        buf.write(u"\u00b7\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00bc\3\2\2")
        buf.write(u"\2\u00bb\u00b9\3\2\2\2\u00bc\u00c0\5\36\20\2\u00bd\u00bf")
        buf.write(u"\7\f\2\2\u00be\u00bd\3\2\2\2\u00bf\u00c2\3\2\2\2\u00c0")
        buf.write(u"\u00be\3\2\2\2\u00c0\u00c1\3\2\2\2\u00c1\u00c3\3\2\2")
        buf.write(u"\2\u00c2\u00c0\3\2\2\2\u00c3\u00c4\7\n\2\2\u00c4\35\3")
        buf.write(u"\2\2\2\u00c5\u00cb\5\n\6\2\u00c6\u00cb\5\20\t\2\u00c7")
        buf.write(u"\u00cb\7\26\2\2\u00c8\u00cb\5\22\n\2\u00c9\u00cb\5\24")
        buf.write(u"\13\2\u00ca\u00c5\3\2\2\2\u00ca\u00c6\3\2\2\2\u00ca\u00c7")
        buf.write(u"\3\2\2\2\u00ca\u00c8\3\2\2\2\u00ca\u00c9\3\2\2\2\u00cb")
        buf.write(u"\37\3\2\2\2\36%+\64;BIOQU\\^bgny}\u0083\u008a\u0091\u0094")
        buf.write(u"\u009a\u009e\u00a4\u00ae\u00b3\u00b9\u00c0\u00ca")
        return buf.getvalue()


class CssParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'*'", u"'|'", u"'.'", u"'['", u"'='", 
                     u"']'", u"':'", u"')'", u"'-'", u"<INVALID>", u"'~='", 
                     u"'|='", u"'^='", u"'$='", u"'*='" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"SPACE", u"INCLUDES", 
                      u"DASHMATCH", u"PREFIXMATCH", u"SUFFIXMATCH", u"SUBSTRINGMATCH", 
                      u"IDENTIFIER", u"STRING", u"FUNCTION", u"NUMBER", 
                      u"HASH", u"PLUS", u"GREATER", u"COMMA", u"TILDE", 
                      u"NOT", u"ATKEYWORD", u"PERCENTAGE", u"DIMENSION" ]

    RULE_selectors_group = 0
    RULE_selector = 1
    RULE_combinator = 2
    RULE_simple_selector_sequence = 3
    RULE_type_selector = 4
    RULE_namespace_prefix = 5
    RULE_element_name = 6
    RULE_universal = 7
    RULE_class_ = 8
    RULE_attribute = 9
    RULE_pseudo = 10
    RULE_functional_pseudo = 11
    RULE_expression = 12
    RULE_negation = 13
    RULE_negation_argument = 14

    ruleNames =  [ u"selectors_group", u"selector", u"combinator", u"simple_selector_sequence", 
                   u"type_selector", u"namespace_prefix", u"element_name", 
                   u"universal", u"class_", u"attribute", u"pseudo", u"functional_pseudo", 
                   u"expression", u"negation", u"negation_argument" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    SPACE=10
    INCLUDES=11
    DASHMATCH=12
    PREFIXMATCH=13
    SUFFIXMATCH=14
    SUBSTRINGMATCH=15
    IDENTIFIER=16
    STRING=17
    FUNCTION=18
    NUMBER=19
    HASH=20
    PLUS=21
    GREATER=22
    COMMA=23
    TILDE=24
    NOT=25
    ATKEYWORD=26
    PERCENTAGE=27
    DIMENSION=28

    def __init__(self, input):
        super(CssParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class Selectors_groupContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Selectors_groupContext, self).__init__(parent, invokingState)
            self.parser = parser

        def selector(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.SelectorContext)
            else:
                return self.getTypedRuleContext(CssParser.SelectorContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(CssParser.COMMA)
            else:
                return self.getToken(CssParser.COMMA, i)

        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def getRuleIndex(self):
            return CssParser.RULE_selectors_group

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterSelectors_group(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitSelectors_group(self)




    def selectors_group(self):

        localctx = CssParser.Selectors_groupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_selectors_group)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.selector()
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.COMMA:
                self.state = 31
                self.match(CssParser.COMMA)
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 32
                    self.match(CssParser.SPACE)
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 38
                self.selector()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SelectorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.SelectorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_selector_sequence(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.Simple_selector_sequenceContext)
            else:
                return self.getTypedRuleContext(CssParser.Simple_selector_sequenceContext,i)


        def combinator(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.CombinatorContext)
            else:
                return self.getTypedRuleContext(CssParser.CombinatorContext,i)


        def getRuleIndex(self):
            return CssParser.RULE_selector

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterSelector(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitSelector(self)




    def selector(self):

        localctx = CssParser.SelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_selector)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.simple_selector_sequence()
            self.state = 50
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.SPACE) | (1 << CssParser.PLUS) | (1 << CssParser.GREATER) | (1 << CssParser.TILDE))) != 0):
                self.state = 45
                self.combinator()
                self.state = 46
                self.simple_selector_sequence()
                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CombinatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.CombinatorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(CssParser.PLUS, 0)

        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def GREATER(self):
            return self.getToken(CssParser.GREATER, 0)

        def TILDE(self):
            return self.getToken(CssParser.TILDE, 0)

        def getRuleIndex(self):
            return CssParser.RULE_combinator

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterCombinator(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitCombinator(self)




    def combinator(self):

        localctx = CssParser.CombinatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_combinator)
        self._la = 0 # Token type
        try:
            self.state = 79
            token = self._input.LA(1)
            if token in [CssParser.PLUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.match(CssParser.PLUS)
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 54
                    self.match(CssParser.SPACE)
                    self.state = 59
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in [CssParser.GREATER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.match(CssParser.GREATER)
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 61
                    self.match(CssParser.SPACE)
                    self.state = 66
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in [CssParser.TILDE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 67
                self.match(CssParser.TILDE)
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 68
                    self.match(CssParser.SPACE)
                    self.state = 73
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in [CssParser.SPACE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 75 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 74
                    self.match(CssParser.SPACE)
                    self.state = 77 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==CssParser.SPACE):
                        break


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_selector_sequenceContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Simple_selector_sequenceContext, self).__init__(parent, invokingState)
            self.parser = parser

        def type_selector(self):
            return self.getTypedRuleContext(CssParser.Type_selectorContext,0)


        def universal(self):
            return self.getTypedRuleContext(CssParser.UniversalContext,0)


        def HASH(self, i=None):
            if i is None:
                return self.getTokens(CssParser.HASH)
            else:
                return self.getToken(CssParser.HASH, i)

        def class_(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.Class_Context)
            else:
                return self.getTypedRuleContext(CssParser.Class_Context,i)


        def attribute(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.AttributeContext)
            else:
                return self.getTypedRuleContext(CssParser.AttributeContext,i)


        def pseudo(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.PseudoContext)
            else:
                return self.getTypedRuleContext(CssParser.PseudoContext,i)


        def negation(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.NegationContext)
            else:
                return self.getTypedRuleContext(CssParser.NegationContext,i)


        def getRuleIndex(self):
            return CssParser.RULE_simple_selector_sequence

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterSimple_selector_sequence(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitSimple_selector_sequence(self)




    def simple_selector_sequence(self):

        localctx = CssParser.Simple_selector_sequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_simple_selector_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 81
                self.type_selector()
                pass

            elif la_ == 2:
                self.state = 82
                self.universal()
                pass


            self.state = 92
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.T__2) | (1 << CssParser.T__3) | (1 << CssParser.T__6) | (1 << CssParser.HASH) | (1 << CssParser.NOT))) != 0):
                self.state = 90
                token = self._input.LA(1)
                if token in [CssParser.HASH]:
                    self.state = 85
                    self.match(CssParser.HASH)

                elif token in [CssParser.T__2]:
                    self.state = 86
                    self.class_()

                elif token in [CssParser.T__3]:
                    self.state = 87
                    self.attribute()

                elif token in [CssParser.T__6]:
                    self.state = 88
                    self.pseudo()

                elif token in [CssParser.NOT]:
                    self.state = 89
                    self.negation()

                else:
                    raise NoViableAltException(self)

                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Type_selectorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Type_selectorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def element_name(self):
            return self.getTypedRuleContext(CssParser.Element_nameContext,0)


        def namespace_prefix(self):
            return self.getTypedRuleContext(CssParser.Namespace_prefixContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_type_selector

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterType_selector(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitType_selector(self)




    def type_selector(self):

        localctx = CssParser.Type_selectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_type_selector)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 95
                self.namespace_prefix()


            self.state = 98
            self.element_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Namespace_prefixContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Namespace_prefixContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CssParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return CssParser.RULE_namespace_prefix

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterNamespace_prefix(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitNamespace_prefix(self)




    def namespace_prefix(self):

        localctx = CssParser.Namespace_prefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_namespace_prefix)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            _la = self._input.LA(1)
            if _la==CssParser.T__0 or _la==CssParser.IDENTIFIER:
                self.state = 100
                _la = self._input.LA(1)
                if not(_la==CssParser.T__0 or _la==CssParser.IDENTIFIER):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()


            self.state = 103
            self.match(CssParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Element_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Element_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CssParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return CssParser.RULE_element_name

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterElement_name(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitElement_name(self)




    def element_name(self):

        localctx = CssParser.Element_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_element_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(CssParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class UniversalContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.UniversalContext, self).__init__(parent, invokingState)
            self.parser = parser

        def namespace_prefix(self):
            return self.getTypedRuleContext(CssParser.Namespace_prefixContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_universal

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterUniversal(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitUniversal(self)




    def universal(self):

        localctx = CssParser.UniversalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_universal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 107
                self.namespace_prefix()


            self.state = 110
            self.match(CssParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Class_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Class_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CssParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return CssParser.RULE_class_

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterClass_(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitClass_(self)




    def class_(self):

        localctx = CssParser.Class_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_class_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(CssParser.T__2)
            self.state = 113
            self.match(CssParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttributeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.AttributeContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i=None):
            if i is None:
                return self.getTokens(CssParser.IDENTIFIER)
            else:
                return self.getToken(CssParser.IDENTIFIER, i)

        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def namespace_prefix(self):
            return self.getTypedRuleContext(CssParser.Namespace_prefixContext,0)


        def PREFIXMATCH(self):
            return self.getToken(CssParser.PREFIXMATCH, 0)

        def SUFFIXMATCH(self):
            return self.getToken(CssParser.SUFFIXMATCH, 0)

        def SUBSTRINGMATCH(self):
            return self.getToken(CssParser.SUBSTRINGMATCH, 0)

        def INCLUDES(self):
            return self.getToken(CssParser.INCLUDES, 0)

        def DASHMATCH(self):
            return self.getToken(CssParser.DASHMATCH, 0)

        def STRING(self):
            return self.getToken(CssParser.STRING, 0)

        def getRuleIndex(self):
            return CssParser.RULE_attribute

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterAttribute(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitAttribute(self)




    def attribute(self):

        localctx = CssParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_attribute)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(CssParser.T__3)
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 116
                self.match(CssParser.SPACE)
                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 123
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.state = 122
                self.namespace_prefix()


            self.state = 125
            self.match(CssParser.IDENTIFIER)
            self.state = 129
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 126
                self.match(CssParser.SPACE)
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 146
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.T__4) | (1 << CssParser.INCLUDES) | (1 << CssParser.DASHMATCH) | (1 << CssParser.PREFIXMATCH) | (1 << CssParser.SUFFIXMATCH) | (1 << CssParser.SUBSTRINGMATCH))) != 0):
                self.state = 132
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.T__4) | (1 << CssParser.INCLUDES) | (1 << CssParser.DASHMATCH) | (1 << CssParser.PREFIXMATCH) | (1 << CssParser.SUFFIXMATCH) | (1 << CssParser.SUBSTRINGMATCH))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 133
                    self.match(CssParser.SPACE)
                    self.state = 138
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 139
                _la = self._input.LA(1)
                if not(_la==CssParser.IDENTIFIER or _la==CssParser.STRING):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 140
                    self.match(CssParser.SPACE)
                    self.state = 145
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 148
            self.match(CssParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PseudoContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.PseudoContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CssParser.IDENTIFIER, 0)

        def functional_pseudo(self):
            return self.getTypedRuleContext(CssParser.Functional_pseudoContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_pseudo

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterPseudo(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitPseudo(self)




    def pseudo(self):

        localctx = CssParser.PseudoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_pseudo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.match(CssParser.T__6)
            self.state = 152
            _la = self._input.LA(1)
            if _la==CssParser.T__6:
                self.state = 151
                self.match(CssParser.T__6)


            self.state = 156
            token = self._input.LA(1)
            if token in [CssParser.IDENTIFIER]:
                self.state = 154
                self.match(CssParser.IDENTIFIER)

            elif token in [CssParser.FUNCTION]:
                self.state = 155
                self.functional_pseudo()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Functional_pseudoContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Functional_pseudoContext, self).__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION(self):
            return self.getToken(CssParser.FUNCTION, 0)

        def expression(self):
            return self.getTypedRuleContext(CssParser.ExpressionContext,0)


        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def getRuleIndex(self):
            return CssParser.RULE_functional_pseudo

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterFunctional_pseudo(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitFunctional_pseudo(self)




    def functional_pseudo(self):

        localctx = CssParser.Functional_pseudoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_functional_pseudo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.match(CssParser.FUNCTION)
            self.state = 162
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 159
                self.match(CssParser.SPACE)
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 165
            self.expression()
            self.state = 166
            self.match(CssParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.ExpressionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self, i=None):
            if i is None:
                return self.getTokens(CssParser.PLUS)
            else:
                return self.getToken(CssParser.PLUS, i)

        def DIMENSION(self, i=None):
            if i is None:
                return self.getTokens(CssParser.DIMENSION)
            else:
                return self.getToken(CssParser.DIMENSION, i)

        def NUMBER(self, i=None):
            if i is None:
                return self.getTokens(CssParser.NUMBER)
            else:
                return self.getToken(CssParser.NUMBER, i)

        def STRING(self, i=None):
            if i is None:
                return self.getTokens(CssParser.STRING)
            else:
                return self.getToken(CssParser.STRING, i)

        def IDENTIFIER(self, i=None):
            if i is None:
                return self.getTokens(CssParser.IDENTIFIER)
            else:
                return self.getToken(CssParser.IDENTIFIER, i)

        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def getRuleIndex(self):
            return CssParser.RULE_expression

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterExpression(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitExpression(self)




    def expression(self):

        localctx = CssParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 168
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.T__8) | (1 << CssParser.IDENTIFIER) | (1 << CssParser.STRING) | (1 << CssParser.NUMBER) | (1 << CssParser.PLUS) | (1 << CssParser.DIMENSION))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 172
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 169
                    self.match(CssParser.SPACE)
                    self.state = 174
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 177 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.T__8) | (1 << CssParser.IDENTIFIER) | (1 << CssParser.STRING) | (1 << CssParser.NUMBER) | (1 << CssParser.PLUS) | (1 << CssParser.DIMENSION))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NegationContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.NegationContext, self).__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(CssParser.NOT, 0)

        def negation_argument(self):
            return self.getTypedRuleContext(CssParser.Negation_argumentContext,0)


        def SPACE(self, i=None):
            if i is None:
                return self.getTokens(CssParser.SPACE)
            else:
                return self.getToken(CssParser.SPACE, i)

        def getRuleIndex(self):
            return CssParser.RULE_negation

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterNegation(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitNegation(self)




    def negation(self):

        localctx = CssParser.NegationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_negation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self.match(CssParser.NOT)
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 180
                self.match(CssParser.SPACE)
                self.state = 185
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 186
            self.negation_argument()
            self.state = 190
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 187
                self.match(CssParser.SPACE)
                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 193
            self.match(CssParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Negation_argumentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Negation_argumentContext, self).__init__(parent, invokingState)
            self.parser = parser

        def type_selector(self):
            return self.getTypedRuleContext(CssParser.Type_selectorContext,0)


        def universal(self):
            return self.getTypedRuleContext(CssParser.UniversalContext,0)


        def HASH(self):
            return self.getToken(CssParser.HASH, 0)

        def class_(self):
            return self.getTypedRuleContext(CssParser.Class_Context,0)


        def attribute(self):
            return self.getTypedRuleContext(CssParser.AttributeContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_negation_argument

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterNegation_argument(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitNegation_argument(self)




    def negation_argument(self):

        localctx = CssParser.Negation_argumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_negation_argument)
        try:
            self.state = 200
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 195
                self.type_selector()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 196
                self.universal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 197
                self.match(CssParser.HASH)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 198
                self.class_()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 199
                self.attribute()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




