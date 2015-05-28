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
        buf.write(u"\17Q\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write(u"\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3")
        buf.write(u"\2\3\2\3\3\5\3\36\n\3\3\3\5\3!\n\3\3\3\5\3$\n\3\3\3\5")
        buf.write(u"\3\'\n\3\3\3\5\3*\n\3\3\3\3\3\5\3.\n\3\3\3\5\3\61\n\3")
        buf.write(u"\3\4\3\4\3\5\3\5\3\5\3\5\5\59\n\5\3\6\3\6\3\7\3\7\3\b")
        buf.write(u"\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13")
        buf.write(u"\3\f\3\f\3\r\3\r\3\r\2\2\16\2\4\6\b\n\f\16\20\22\24\26")
        buf.write(u"\30\2\4\3\2\n\13\3\2\f\rL\2\32\3\2\2\2\4\35\3\2\2\2\6")
        buf.write(u"\62\3\2\2\2\b8\3\2\2\2\n:\3\2\2\2\f<\3\2\2\2\16>\3\2")
        buf.write(u"\2\2\20A\3\2\2\2\22D\3\2\2\2\24J\3\2\2\2\26L\3\2\2\2")
        buf.write(u"\30N\3\2\2\2\32\33\5\4\3\2\33\3\3\2\2\2\34\36\5\6\4\2")
        buf.write(u"\35\34\3\2\2\2\35\36\3\2\2\2\36 \3\2\2\2\37!\5\b\5\2")
        buf.write(u" \37\3\2\2\2 !\3\2\2\2!#\3\2\2\2\"$\5\20\t\2#\"\3\2\2")
        buf.write(u"\2#$\3\2\2\2$&\3\2\2\2%\'\5\16\b\2&%\3\2\2\2&\'\3\2\2")
        buf.write(u"\2\')\3\2\2\2(*\5\22\n\2)(\3\2\2\2)*\3\2\2\2*-\3\2\2")
        buf.write(u"\2+,\7\17\2\2,.\5\4\3\2-+\3\2\2\2-.\3\2\2\2.\60\3\2\2")
        buf.write(u"\2/\61\7\3\2\2\60/\3\2\2\2\60\61\3\2\2\2\61\5\3\2\2\2")
        buf.write(u"\62\63\7\f\2\2\63\7\3\2\2\2\64\65\7\4\2\2\659\5\n\6\2")
        buf.write(u"\66\67\7\5\2\2\679\5\f\7\28\64\3\2\2\28\66\3\2\2\29\t")
        buf.write(u"\3\2\2\2:;\7\f\2\2;\13\3\2\2\2<=\7\f\2\2=\r\3\2\2\2>")
        buf.write(u"?\7\6\2\2?@\7\f\2\2@\17\3\2\2\2AB\7\7\2\2BC\7\f\2\2C")
        buf.write(u"\21\3\2\2\2DE\7\b\2\2EF\5\24\13\2FG\5\26\f\2GH\5\30\r")
        buf.write(u"\2HI\7\t\2\2I\23\3\2\2\2JK\7\f\2\2K\25\3\2\2\2LM\t\2")
        buf.write(u"\2\2M\27\3\2\2\2NO\t\3\2\2O\31\3\2\2\2\n\35 #&)-\608")
        return buf.getvalue()


class CssParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'\n'", u"'.'", u"'#'", u"':'", u"'::'", 
                     u"'['", u"']'", u"'='", u"'^='" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"IDENT", u"VALUE", u"IDCHAR", 
                      u"SPACE" ]

    RULE_selector = 0
    RULE_node = 1
    RULE_element = 2
    RULE_qualifier = 3
    RULE_klazz = 4
    RULE_ident = 5
    RULE_pseudoclass = 6
    RULE_prop = 7
    RULE_attr = 8
    RULE_attrname = 9
    RULE_rel = 10
    RULE_attrvalue = 11

    ruleNames =  [ u"selector", u"node", u"element", u"qualifier", u"klazz", 
                   u"ident", u"pseudoclass", u"prop", u"attr", u"attrname", 
                   u"rel", u"attrvalue" ]

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
    IDENT=10
    VALUE=11
    IDCHAR=12
    SPACE=13

    def __init__(self, input):
        super(CssParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class SelectorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.SelectorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def node(self):
            return self.getTypedRuleContext(CssParser.NodeContext,0)


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
        self.enterRule(localctx, 0, self.RULE_selector)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.node()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NodeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.NodeContext, self).__init__(parent, invokingState)
            self.parser = parser

        def element(self):
            return self.getTypedRuleContext(CssParser.ElementContext,0)


        def qualifier(self):
            return self.getTypedRuleContext(CssParser.QualifierContext,0)


        def prop(self):
            return self.getTypedRuleContext(CssParser.PropContext,0)


        def pseudoclass(self):
            return self.getTypedRuleContext(CssParser.PseudoclassContext,0)


        def attr(self):
            return self.getTypedRuleContext(CssParser.AttrContext,0)


        def SPACE(self):
            return self.getToken(CssParser.SPACE, 0)

        def node(self):
            return self.getTypedRuleContext(CssParser.NodeContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_node

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterNode(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitNode(self)




    def node(self):

        localctx = CssParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_node)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            _la = self._input.LA(1)
            if _la==CssParser.IDENT:
                self.state = 26
                self.element()


            self.state = 30
            _la = self._input.LA(1)
            if _la==CssParser.T__1 or _la==CssParser.T__2:
                self.state = 29
                self.qualifier()


            self.state = 33
            _la = self._input.LA(1)
            if _la==CssParser.T__4:
                self.state = 32
                self.prop()


            self.state = 36
            _la = self._input.LA(1)
            if _la==CssParser.T__3:
                self.state = 35
                self.pseudoclass()


            self.state = 39
            _la = self._input.LA(1)
            if _la==CssParser.T__5:
                self.state = 38
                self.attr()


            self.state = 43
            _la = self._input.LA(1)
            if _la==CssParser.SPACE:
                self.state = 41
                self.match(CssParser.SPACE)
                self.state = 42
                self.node()


            self.state = 46
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 45
                self.match(CssParser.T__0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ElementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.ElementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_element

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterElement(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitElement(self)




    def element(self):

        localctx = CssParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class QualifierContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.QualifierContext, self).__init__(parent, invokingState)
            self.parser = parser

        def klazz(self):
            return self.getTypedRuleContext(CssParser.KlazzContext,0)


        def ident(self):
            return self.getTypedRuleContext(CssParser.IdentContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_qualifier

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterQualifier(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitQualifier(self)




    def qualifier(self):

        localctx = CssParser.QualifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_qualifier)
        try:
            self.state = 54
            token = self._input.LA(1)
            if token in [CssParser.T__1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.match(CssParser.T__1)
                self.state = 51
                self.klazz()

            elif token in [CssParser.T__2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(CssParser.T__2)
                self.state = 53
                self.ident()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class KlazzContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.KlazzContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_klazz

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterKlazz(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitKlazz(self)




    def klazz(self):

        localctx = CssParser.KlazzContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_klazz)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.IdentContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_ident

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterIdent(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitIdent(self)




    def ident(self):

        localctx = CssParser.IdentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ident)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PseudoclassContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.PseudoclassContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_pseudoclass

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterPseudoclass(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitPseudoclass(self)




    def pseudoclass(self):

        localctx = CssParser.PseudoclassContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_pseudoclass)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(CssParser.T__3)
            self.state = 61
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PropContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.PropContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_prop

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterProp(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitProp(self)




    def prop(self):

        localctx = CssParser.PropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_prop)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(CssParser.T__4)
            self.state = 64
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttrContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.AttrContext, self).__init__(parent, invokingState)
            self.parser = parser

        def attrname(self):
            return self.getTypedRuleContext(CssParser.AttrnameContext,0)


        def rel(self):
            return self.getTypedRuleContext(CssParser.RelContext,0)


        def attrvalue(self):
            return self.getTypedRuleContext(CssParser.AttrvalueContext,0)


        def getRuleIndex(self):
            return CssParser.RULE_attr

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterAttr(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitAttr(self)




    def attr(self):

        localctx = CssParser.AttrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_attr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(CssParser.T__5)
            self.state = 67
            self.attrname()
            self.state = 68
            self.rel()
            self.state = 69
            self.attrvalue()
            self.state = 70
            self.match(CssParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttrnameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.AttrnameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def getRuleIndex(self):
            return CssParser.RULE_attrname

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterAttrname(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitAttrname(self)




    def attrname(self):

        localctx = CssParser.AttrnameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_attrname)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(CssParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RelContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.RelContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CssParser.RULE_rel

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterRel(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitRel(self)




    def rel(self):

        localctx = CssParser.RelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_rel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            _la = self._input.LA(1)
            if not(_la==CssParser.T__7 or _la==CssParser.T__8):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttrvalueContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(CssParser.AttrvalueContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(CssParser.IDENT, 0)

        def VALUE(self):
            return self.getToken(CssParser.VALUE, 0)

        def getRuleIndex(self):
            return CssParser.RULE_attrvalue

        def enterRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.enterAttrvalue(self)

        def exitRule(self, listener):
            if isinstance( listener, CssListener ):
                listener.exitAttrvalue(self)




    def attrvalue(self):

        localctx = CssParser.AttrvalueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_attrvalue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            _la = self._input.LA(1)
            if not(_la==CssParser.IDENT or _la==CssParser.VALUE):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




