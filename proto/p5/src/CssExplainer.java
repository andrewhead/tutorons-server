import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;


public class CssExplainer extends CssBaseListener {

    ParseTreeProperty<PhraseElement> phrases = new ParseTreeProperty<PhraseElement>();
    Lexicon lexicon = Lexicon.getDefaultLexicon();
    NLGFactory factory = new NLGFactory(lexicon);
    Realiser realiser = new Realiser(lexicon);


    public static void main(String [] args) {

        String[] testStrings = {
            "div.featured a",
            "div#footer_inner strong",
            "div.video-summary-data a[href^=/video]",
            "p.introduction::text",
            "div#videobox h3",
            ".watch-view-count"
        };

        for (int i = 0; i < testStrings.length; i++) {
            String string = testStrings[i];
            ANTLRInputStream input = new ANTLRInputStream(string);
            CssLexer lexer = new CssLexer(input);
            CommonTokenStream tokens = new CommonTokenStream(lexer);
            CssParser parser = new CssParser(tokens);
            ParseTree tree = parser.selector();
            ParseTreeWalker walker = new ParseTreeWalker();
            walker.walk(new CssExplainer(), tree);
        }

    }

    public void exitSelector(CssParser.SelectorContext ctx) {

        SPhraseSpec sentence = factory.createClause();
        NPPhraseSpec noun = factory.createNounPhrase("selector");
        noun.setDeterminer("the");
        noun.addPostModifier("'" + ctx.getText() + "'");
        sentence.setSubject(noun);
        sentence.setVerb("choose");
        sentence.setComplement(phrases.get(ctx.node()));
        System.out.println(realiser.realiseSentence(sentence));

    }

    public NPPhraseSpec getTagNoun(String tag) {

        if (tag.equals("h3")) {
            NPPhraseSpec noun = factory.createNounPhrase("header");
            noun.addPostModifier("(of level 3)");
            return noun;
        } else {
            String string;
            if (tag.equals("p")) string = "paragraph";
            else if (tag.equals("div")) string ="container";
            else if (tag.equals("strong")) string ="bolded text";
            else if (tag.equals("a")) string = "link";
            else string = tag;
            return factory.createNounPhrase(string);
        }

    }

    public NPPhraseSpec getPropertyNoun(String prop) {
        return factory.createNounPhrase(prop);
    }

    public void exitNode(CssParser.NodeContext ctx) {

        /* Prepare description of tag */
        NPPhraseSpec tagNoun;
        if (ctx.selection().element() != null) {
            String tag = ctx.selection().element().IDENT().getText();
            tagNoun = getTagNoun(tag);
        } else {
            tagNoun = factory.createNounPhrase("element");
        }

        if (ctx.selection().qualifier() != null) {
            CssParser.QualifierContext qualifier = ctx.selection().qualifier();
            if (qualifier.id() != null) {
                tagNoun.addPostModifier("with the ID '" + qualifier.id().IDENT().getText() + "'");
                tagNoun.setDeterminer("a");
            } else if (qualifier.klazz() != null) {
                tagNoun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
                tagNoun.addPostModifier("of class '" + qualifier.klazz().IDENT().getText() + "'");
            }
        } else {
            tagNoun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
        }

        /* Choose the noun of the node as the property of the node, if it exists, otherwise the tag itself */
        NPPhraseSpec nodeNoun;
        if (ctx.property() == null) {
            nodeNoun = tagNoun;
        } else {
            String prop = ctx.property().IDENT().getText();
            nodeNoun = getPropertyNoun(prop);
            nodeNoun.addPostModifier("from");
            nodeNoun.addPostModifier(tagNoun);
        }

        /* Describe attributes */
        if (ctx.attr() != null) {
            nodeNoun.addPostModifier("with");
            NPPhraseSpec attrPhrase = (NPPhraseSpec) phrases.get(ctx.attr());
            if (nodeNoun.getFeature(Feature.NUMBER) == NumberAgreement.PLURAL) {
                attrPhrase.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
            }
            nodeNoun.addPostModifier(attrPhrase);
        }

        /* Place focus of phrase on the child if one exists */
        if (ctx.node() != null) {
            PhraseElement childPhrase = phrases.get(ctx.node());
            childPhrase.addPostModifier("from");
            childPhrase.addPostModifier(nodeNoun);
            phrases.put(ctx, childPhrase);
        }
        else {
            phrases.put(ctx, nodeNoun);
        }

    }

    public void exitAttr(CssParser.AttrContext ctx) {

        NPPhraseSpec noun = factory.createNounPhrase();
        if (ctx.attrname().getText().equals("href")) {
            noun.setNoun("URL");
        } else {
            noun.setNoun(ctx.attrname().getText());
        }

        if (ctx.rel().getText().equals("^=")) {
            noun.addPostModifier("starting with");
        } else {
            noun.addPostModifier("related to");
        }

        noun.addPostModifier("'" + ctx.attrvalue().getText() + "'");
        phrases.put(ctx, noun);

    }

}