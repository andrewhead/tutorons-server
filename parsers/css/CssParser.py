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
        buf.write(u"\36\u00d3\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\3\2\3")
        buf.write(u"\2\7\2&\n\2\f\2\16\2)\13\2\3\2\7\2,\n\2\f\2\16\2/\13")
        buf.write(u"\2\3\3\3\3\3\3\3\3\7\3\65\n\3\f\3\16\38\13\3\3\4\3\4")
        buf.write(u"\7\4<\n\4\f\4\16\4?\13\4\3\4\3\4\7\4C\n\4\f\4\16\4F\13")
        buf.write(u"\4\3\4\3\4\7\4J\n\4\f\4\16\4M\13\4\3\4\6\4P\n\4\r\4\16")
        buf.write(u"\4Q\5\4T\n\4\3\5\3\5\5\5X\n\5\3\5\3\5\3\5\3\5\3\5\7\5")
        buf.write(u"_\n\5\f\5\16\5b\13\5\3\6\5\6e\n\6\3\6\3\6\3\7\5\7j\n")
        buf.write(u"\7\3\7\3\7\3\b\3\b\3\t\5\tq\n\t\3\t\3\t\5\tu\n\t\3\n")
        buf.write(u"\3\n\3\13\3\13\3\13\3\f\3\f\7\f~\n\f\f\f\16\f\u0081\13")
        buf.write(u"\f\3\f\5\f\u0084\n\f\3\f\3\f\7\f\u0088\n\f\f\f\16\f\u008b")
        buf.write(u"\13\f\3\f\3\f\7\f\u008f\n\f\f\f\16\f\u0092\13\f\3\f\3")
        buf.write(u"\f\7\f\u0096\n\f\f\f\16\f\u0099\13\f\5\f\u009b\n\f\3")
        buf.write(u"\f\3\f\3\r\3\r\5\r\u00a1\n\r\3\r\3\r\5\r\u00a5\n\r\3")
        buf.write(u"\16\3\16\7\16\u00a9\n\16\f\16\16\16\u00ac\13\16\3\16")
        buf.write(u"\3\16\3\16\3\17\3\17\7\17\u00b3\n\17\f\17\16\17\u00b6")
        buf.write(u"\13\17\6\17\u00b8\n\17\r\17\16\17\u00b9\3\20\3\20\7\20")
        buf.write(u"\u00be\n\20\f\20\16\20\u00c1\13\20\3\20\3\20\7\20\u00c5")
        buf.write(u"\n\20\f\20\16\20\u00c8\13\20\3\20\3\20\3\21\3\21\3\21")
        buf.write(u"\3\21\3\21\5\21\u00d1\n\21\3\21\2\2\22\2\4\6\b\n\f\16")
        buf.write(u"\20\22\24\26\30\32\34\36 \2\6\4\2\t\t\26\26\4\2\4\b\30")
        buf.write(u"\30\3\2\t\n\6\2\t\n\f\r\24\24\27\27\u00e7\2\"\3\2\2\2")
        buf.write(u"\4\60\3\2\2\2\6S\3\2\2\2\bW\3\2\2\2\nd\3\2\2\2\fi\3\2")
        buf.write(u"\2\2\16m\3\2\2\2\20t\3\2\2\2\22v\3\2\2\2\24x\3\2\2\2")
        buf.write(u"\26{\3\2\2\2\30\u009e\3\2\2\2\32\u00a6\3\2\2\2\34\u00b7")
        buf.write(u"\3\2\2\2\36\u00bb\3\2\2\2 \u00d0\3\2\2\2\"-\5\4\3\2#")
        buf.write(u"\'\7\17\2\2$&\7\3\2\2%$\3\2\2\2&)\3\2\2\2\'%\3\2\2\2")
        buf.write(u"\'(\3\2\2\2(*\3\2\2\2)\'\3\2\2\2*,\5\4\3\2+#\3\2\2\2")
        buf.write(u",/\3\2\2\2-+\3\2\2\2-.\3\2\2\2.\3\3\2\2\2/-\3\2\2\2\60")
        buf.write(u"\66\5\b\5\2\61\62\5\6\4\2\62\63\5\b\5\2\63\65\3\2\2\2")
        buf.write(u"\64\61\3\2\2\2\658\3\2\2\2\66\64\3\2\2\2\66\67\3\2\2")
        buf.write(u"\2\67\5\3\2\2\28\66\3\2\2\29=\7\r\2\2:<\7\3\2\2;:\3\2")
        buf.write(u"\2\2<?\3\2\2\2=;\3\2\2\2=>\3\2\2\2>T\3\2\2\2?=\3\2\2")
        buf.write(u"\2@D\7\16\2\2AC\7\3\2\2BA\3\2\2\2CF\3\2\2\2DB\3\2\2\2")
        buf.write(u"DE\3\2\2\2ET\3\2\2\2FD\3\2\2\2GK\7\20\2\2HJ\7\3\2\2I")
        buf.write(u"H\3\2\2\2JM\3\2\2\2KI\3\2\2\2KL\3\2\2\2LT\3\2\2\2MK\3")
        buf.write(u"\2\2\2NP\7\3\2\2ON\3\2\2\2PQ\3\2\2\2QO\3\2\2\2QR\3\2")
        buf.write(u"\2\2RT\3\2\2\2S9\3\2\2\2S@\3\2\2\2SG\3\2\2\2SO\3\2\2")
        buf.write(u"\2T\7\3\2\2\2UX\5\n\6\2VX\5\20\t\2WU\3\2\2\2WV\3\2\2")
        buf.write(u"\2X`\3\2\2\2Y_\5\22\n\2Z_\5\24\13\2[_\5\26\f\2\\_\5\30")
        buf.write(u"\r\2]_\5\36\20\2^Y\3\2\2\2^Z\3\2\2\2^[\3\2\2\2^\\\3\2")
        buf.write(u"\2\2^]\3\2\2\2_b\3\2\2\2`^\3\2\2\2`a\3\2\2\2a\t\3\2\2")
        buf.write(u"\2b`\3\2\2\2ce\5\f\7\2dc\3\2\2\2de\3\2\2\2ef\3\2\2\2")
        buf.write(u"fg\5\16\b\2g\13\3\2\2\2hj\t\2\2\2ih\3\2\2\2ij\3\2\2\2")
        buf.write(u"jk\3\2\2\2kl\7\31\2\2l\r\3\2\2\2mn\7\t\2\2n\17\3\2\2")
        buf.write(u"\2oq\5\f\7\2po\3\2\2\2pq\3\2\2\2qr\3\2\2\2ru\7\26\2\2")
        buf.write(u"su\3\2\2\2tp\3\2\2\2ts\3\2\2\2u\21\3\2\2\2vw\7\36\2\2")
        buf.write(u"w\23\3\2\2\2xy\7\32\2\2yz\7\t\2\2z\25\3\2\2\2{\177\7")
        buf.write(u"\33\2\2|~\7\3\2\2}|\3\2\2\2~\u0081\3\2\2\2\177}\3\2\2")
        buf.write(u"\2\177\u0080\3\2\2\2\u0080\u0083\3\2\2\2\u0081\177\3")
        buf.write(u"\2\2\2\u0082\u0084\5\f\7\2\u0083\u0082\3\2\2\2\u0083")
        buf.write(u"\u0084\3\2\2\2\u0084\u0085\3\2\2\2\u0085\u0089\7\t\2")
        buf.write(u"\2\u0086\u0088\7\3\2\2\u0087\u0086\3\2\2\2\u0088\u008b")
        buf.write(u"\3\2\2\2\u0089\u0087\3\2\2\2\u0089\u008a\3\2\2\2\u008a")
        buf.write(u"\u009a\3\2\2\2\u008b\u0089\3\2\2\2\u008c\u0090\t\3\2")
        buf.write(u"\2\u008d\u008f\7\3\2\2\u008e\u008d\3\2\2\2\u008f\u0092")
        buf.write(u"\3\2\2\2\u0090\u008e\3\2\2\2\u0090\u0091\3\2\2\2\u0091")
        buf.write(u"\u0093\3\2\2\2\u0092\u0090\3\2\2\2\u0093\u0097\t\4\2")
        buf.write(u"\2\u0094\u0096\7\3\2\2\u0095\u0094\3\2\2\2\u0096\u0099")
        buf.write(u"\3\2\2\2\u0097\u0095\3\2\2\2\u0097\u0098\3\2\2\2\u0098")
        buf.write(u"\u009b\3\2\2\2\u0099\u0097\3\2\2\2\u009a\u008c\3\2\2")
        buf.write(u"\2\u009a\u009b\3\2\2\2\u009b\u009c\3\2\2\2\u009c\u009d")
        buf.write(u"\7\34\2\2\u009d\27\3\2\2\2\u009e\u00a0\7\25\2\2\u009f")
        buf.write(u"\u00a1\7\25\2\2\u00a0\u009f\3\2\2\2\u00a0\u00a1\3\2\2")
        buf.write(u"\2\u00a1\u00a4\3\2\2\2\u00a2\u00a5\7\t\2\2\u00a3\u00a5")
        buf.write(u"\5\32\16\2\u00a4\u00a2\3\2\2\2\u00a4\u00a3\3\2\2\2\u00a5")
        buf.write(u"\31\3\2\2\2\u00a6\u00aa\7\13\2\2\u00a7\u00a9\7\3\2\2")
        buf.write(u"\u00a8\u00a7\3\2\2\2\u00a9\u00ac\3\2\2\2\u00aa\u00a8")
        buf.write(u"\3\2\2\2\u00aa\u00ab\3\2\2\2\u00ab\u00ad\3\2\2\2\u00ac")
        buf.write(u"\u00aa\3\2\2\2\u00ad\u00ae\5\34\17\2\u00ae\u00af\7\35")
        buf.write(u"\2\2\u00af\33\3\2\2\2\u00b0\u00b4\t\5\2\2\u00b1\u00b3")
        buf.write(u"\7\3\2\2\u00b2\u00b1\3\2\2\2\u00b3\u00b6\3\2\2\2\u00b4")
        buf.write(u"\u00b2\3\2\2\2\u00b4\u00b5\3\2\2\2\u00b5\u00b8\3\2\2")
        buf.write(u"\2\u00b6\u00b4\3\2\2\2\u00b7\u00b0\3\2\2\2\u00b8\u00b9")
        buf.write(u"\3\2\2\2\u00b9\u00b7\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba")
        buf.write(u"\35\3\2\2\2\u00bb\u00bf\7\21\2\2\u00bc\u00be\7\3\2\2")
        buf.write(u"\u00bd\u00bc\3\2\2\2\u00be\u00c1\3\2\2\2\u00bf\u00bd")
        buf.write(u"\3\2\2\2\u00bf\u00c0\3\2\2\2\u00c0\u00c2\3\2\2\2\u00c1")
        buf.write(u"\u00bf\3\2\2\2\u00c2\u00c6\5 \21\2\u00c3\u00c5\7\3\2")
        buf.write(u"\2\u00c4\u00c3\3\2\2\2\u00c5\u00c8\3\2\2\2\u00c6\u00c4")
        buf.write(u"\3\2\2\2\u00c6\u00c7\3\2\2\2\u00c7\u00c9\3\2\2\2\u00c8")
        buf.write(u"\u00c6\3\2\2\2\u00c9\u00ca\7\35\2\2\u00ca\37\3\2\2\2")
        buf.write(u"\u00cb\u00d1\5\n\6\2\u00cc\u00d1\5\20\t\2\u00cd\u00d1")
        buf.write(u"\5\22\n\2\u00ce\u00d1\5\24\13\2\u00cf\u00d1\5\26\f\2")
        buf.write(u"\u00d0\u00cb\3\2\2\2\u00d0\u00cc\3\2\2\2\u00d0\u00cd")
        buf.write(u"\3\2\2\2\u00d0\u00ce\3\2\2\2\u00d0\u00cf\3\2\2\2\u00d1")
        buf.write(u"!\3\2\2\2\37\'-\66=DKQSW^`dipt\177\u0083\u0089\u0090")
        buf.write(u"\u0097\u009a\u00a0\u00a4\u00aa\u00b4\u00b9\u00bf\u00c6")
        buf.write(u"\u00d0")
        return buf.getvalue()


class CssParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"<INVALID>", u"'~='", u"'|='", u"'^='", 
                     u"'$='", u"'*='", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"<INVALID>", u"':'", u"'*'", u"'-'", u"'='", u"'|'", 
                     u"'.'", u"'['", u"']'", u"')'" ]

    symbolicNames = [ u"<INVALID>", u"SPACE", u"INCLUDES", u"DASHMATCH", 
                      u"PREFIXMATCH", u"SUFFIXMATCH", u"SUBSTRINGMATCH", 
                      u"IDENTIFIER", u"STRING", u"FUNCTION", u"NUMBER", 
                      u"PLUS", u"GREATER", u"COMMA", u"TILDE", u"NOT", u"ATKEYWORD", 
                      u"PERCENTAGE", u"DIMENSION", u"COLON", u"STAR", u"DASH", 
                      u"EQUALS", u"BAR", u"DOT", u"LEFT_BRACKET", u"RIGHT_BRACKET", 
                      u"RIGHT_PARENTHESIS", u"HASH" ]

    RULE_selectors_group = 0
    RULE_selector = 1
    RULE_combinator = 2
    RULE_simple_selector_sequence = 3
    RULE_type_selector = 4
    RULE_namespace_prefix = 5
    RULE_element_name = 6
    RULE_universal = 7
    RULE_hash_ = 8
    RULE_class_ = 9
    RULE_attribute = 10
    RULE_pseudo = 11
    RULE_functional_pseudo = 12
    RULE_expression = 13
    RULE_negation = 14
    RULE_negation_argument = 15

    ruleNames =  [ u"selectors_group", u"selector", u"combinator", u"simple_selector_sequence", 
                   u"type_selector", u"namespace_prefix", u"element_name", 
                   u"universal", u"hash_", u"class_", u"attribute", u"pseudo", 
                   u"functional_pseudo", u"expression", u"negation", u"negation_argument" ]

    EOF = Token.EOF
    SPACE=1
    INCLUDES=2
    DASHMATCH=3
    PREFIXMATCH=4
    SUFFIXMATCH=5
    SUBSTRINGMATCH=6
    IDENTIFIER=7
    STRING=8
    FUNCTION=9
    NUMBER=10
    PLUS=11
    GREATER=12
    COMMA=13
    TILDE=14
    NOT=15
    ATKEYWORD=16
    PERCENTAGE=17
    DIMENSION=18
    COLON=19
    STAR=20
    DASH=21
    EQUALS=22
    BAR=23
    DOT=24
    LEFT_BRACKET=25
    RIGHT_BRACKET=26
    RIGHT_PARENTHESIS=27
    HASH=28

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
            self.state = 32
            self.selector()
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.COMMA:
                self.state = 33
                self.match(CssParser.COMMA)
                self.state = 37
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 34
                        self.match(CssParser.SPACE) 
                    self.state = 39
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

                self.state = 40
                self.selector()
                self.state = 45
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
            self.state = 46
            self.simple_selector_sequence()
            self.state = 52
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.SPACE) | (1 << CssParser.PLUS) | (1 << CssParser.GREATER) | (1 << CssParser.TILDE))) != 0):
                self.state = 47
                self.combinator()
                self.state = 48
                self.simple_selector_sequence()
                self.state = 54
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
        try:
            self.state = 81
            token = self._input.LA(1)
            if token in [CssParser.PLUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 55
                self.match(CssParser.PLUS)
                self.state = 59
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 56
                        self.match(CssParser.SPACE) 
                    self.state = 61
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,3,self._ctx)


            elif token in [CssParser.GREATER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 62
                self.match(CssParser.GREATER)
                self.state = 66
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 63
                        self.match(CssParser.SPACE) 
                    self.state = 68
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,4,self._ctx)


            elif token in [CssParser.TILDE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 69
                self.match(CssParser.TILDE)
                self.state = 73
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 70
                        self.match(CssParser.SPACE) 
                    self.state = 75
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,5,self._ctx)


            elif token in [CssParser.SPACE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 77 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 76
                        self.match(CssParser.SPACE)

                    else:
                        raise NoViableAltException(self)
                    self.state = 79 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,6,self._ctx)


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


        def hash_(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(CssParser.Hash_Context)
            else:
                return self.getTypedRuleContext(CssParser.Hash_Context,i)


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
            self.state = 85
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 83
                self.type_selector()
                pass

            elif la_ == 2:
                self.state = 84
                self.universal()
                pass


            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.NOT) | (1 << CssParser.COLON) | (1 << CssParser.DOT) | (1 << CssParser.LEFT_BRACKET) | (1 << CssParser.HASH))) != 0):
                self.state = 92
                token = self._input.LA(1)
                if token in [CssParser.HASH]:
                    self.state = 87
                    self.hash_()

                elif token in [CssParser.DOT]:
                    self.state = 88
                    self.class_()

                elif token in [CssParser.LEFT_BRACKET]:
                    self.state = 89
                    self.attribute()

                elif token in [CssParser.COLON]:
                    self.state = 90
                    self.pseudo()

                elif token in [CssParser.NOT]:
                    self.state = 91
                    self.negation()

                else:
                    raise NoViableAltException(self)

                self.state = 96
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
            self.state = 98
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 97
                self.namespace_prefix()


            self.state = 100
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

        def BAR(self):
            return self.getToken(CssParser.BAR, 0)

        def IDENTIFIER(self):
            return self.getToken(CssParser.IDENTIFIER, 0)

        def STAR(self):
            return self.getToken(CssParser.STAR, 0)

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
            self.state = 103
            _la = self._input.LA(1)
            if _la==CssParser.IDENTIFIER or _la==CssParser.STAR:
                self.state = 102
                _la = self._input.LA(1)
                if not(_la==CssParser.IDENTIFIER or _la==CssParser.STAR):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()


            self.state = 105
            self.match(CssParser.BAR)
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
            self.state = 107
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

        def STAR(self):
            return self.getToken(CssParser.STAR, 0)

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
            self.state = 114
            token = self._input.LA(1)
            if token in [CssParser.IDENTIFIER, CssParser.STAR, CssParser.BAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 110
                la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                if la_ == 1:
                    self.state = 109
                    self.namespace_prefix()


                self.state = 112
                self.match(CssParser.STAR)

            elif token in [CssParser.EOF, CssParser.SPACE, CssParser.PLUS, CssParser.GREATER, CssParser.COMMA, CssParser.TILDE, CssParser.NOT, CssParser.COLON, CssParser.DOT, CssParser.LEFT_BRACKET, CssParser.RIGHT_PARENTHESIS, CssParser.HASH]:
                self.enterOuterAlt(localctx, 2)


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Hash_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.Hash_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def HASH(self):
            return self.getToken(CssParser.HASH, 0)

        def getRuleIndex(self):
            return CssParser.RULE_hash_

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterHash_(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitHash_(self)




    def hash_(self):

        localctx = CssParser.Hash_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_hash_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(CssParser.HASH)
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

        def DOT(self):
            return self.getToken(CssParser.DOT, 0)

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
        self.enterRule(localctx, 18, self.RULE_class_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(CssParser.DOT)
            self.state = 119
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

        def LEFT_BRACKET(self):
            return self.getToken(CssParser.LEFT_BRACKET, 0)

        def IDENTIFIER(self, i=None):
            if i is None:
                return self.getTokens(CssParser.IDENTIFIER)
            else:
                return self.getToken(CssParser.IDENTIFIER, i)

        def RIGHT_BRACKET(self):
            return self.getToken(CssParser.RIGHT_BRACKET, 0)

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

        def EQUALS(self):
            return self.getToken(CssParser.EQUALS, 0)

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
        self.enterRule(localctx, 20, self.RULE_attribute)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            self.match(CssParser.LEFT_BRACKET)
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 122
                self.match(CssParser.SPACE)
                self.state = 127
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 129
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.state = 128
                self.namespace_prefix()


            self.state = 131
            self.match(CssParser.IDENTIFIER)
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 132
                self.match(CssParser.SPACE)
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 152
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.INCLUDES) | (1 << CssParser.DASHMATCH) | (1 << CssParser.PREFIXMATCH) | (1 << CssParser.SUFFIXMATCH) | (1 << CssParser.SUBSTRINGMATCH) | (1 << CssParser.EQUALS))) != 0):
                self.state = 138
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.INCLUDES) | (1 << CssParser.DASHMATCH) | (1 << CssParser.PREFIXMATCH) | (1 << CssParser.SUFFIXMATCH) | (1 << CssParser.SUBSTRINGMATCH) | (1 << CssParser.EQUALS))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 139
                    self.match(CssParser.SPACE)
                    self.state = 144
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 145
                _la = self._input.LA(1)
                if not(_la==CssParser.IDENTIFIER or _la==CssParser.STRING):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 149
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 146
                    self.match(CssParser.SPACE)
                    self.state = 151
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 154
            self.match(CssParser.RIGHT_BRACKET)
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

        def COLON(self, i=None):
            if i is None:
                return self.getTokens(CssParser.COLON)
            else:
                return self.getToken(CssParser.COLON, i)

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
        self.enterRule(localctx, 22, self.RULE_pseudo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(CssParser.COLON)
            self.state = 158
            _la = self._input.LA(1)
            if _la==CssParser.COLON:
                self.state = 157
                self.match(CssParser.COLON)


            self.state = 162
            token = self._input.LA(1)
            if token in [CssParser.IDENTIFIER]:
                self.state = 160
                self.match(CssParser.IDENTIFIER)

            elif token in [CssParser.FUNCTION]:
                self.state = 161
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


        def RIGHT_PARENTHESIS(self):
            return self.getToken(CssParser.RIGHT_PARENTHESIS, 0)

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
        self.enterRule(localctx, 24, self.RULE_functional_pseudo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(CssParser.FUNCTION)
            self.state = 168
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 165
                self.match(CssParser.SPACE)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 171
            self.expression()
            self.state = 172
            self.match(CssParser.RIGHT_PARENTHESIS)
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
        self.enterRule(localctx, 26, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 174
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.IDENTIFIER) | (1 << CssParser.STRING) | (1 << CssParser.NUMBER) | (1 << CssParser.PLUS) | (1 << CssParser.DIMENSION) | (1 << CssParser.DASH))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 178
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CssParser.SPACE:
                    self.state = 175
                    self.match(CssParser.SPACE)
                    self.state = 180
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 183 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CssParser.IDENTIFIER) | (1 << CssParser.STRING) | (1 << CssParser.NUMBER) | (1 << CssParser.PLUS) | (1 << CssParser.DIMENSION) | (1 << CssParser.DASH))) != 0)):
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


        def RIGHT_PARENTHESIS(self):
            return self.getToken(CssParser.RIGHT_PARENTHESIS, 0)

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
        self.enterRule(localctx, 28, self.RULE_negation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(CssParser.NOT)
            self.state = 189
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,26,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 186
                    self.match(CssParser.SPACE) 
                self.state = 191
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,26,self._ctx)

            self.state = 192
            self.negation_argument()
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CssParser.SPACE:
                self.state = 193
                self.match(CssParser.SPACE)
                self.state = 198
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 199
            self.match(CssParser.RIGHT_PARENTHESIS)
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


        def hash_(self):
            return self.getTypedRuleContext(CssParser.Hash_Context,0)


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
        self.enterRule(localctx, 30, self.RULE_negation_argument)
        try:
            self.state = 206
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 201
                self.type_selector()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 202
                self.universal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 203
                self.hash_()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 204
                self.class_()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 205
                self.attribute()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




