import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class CssExplainer extends CssBaseListener {

    ParseTreeProperty<PhraseElement> phrases = new ParseTreeProperty<PhraseElement>();
    Lexicon lexicon = Lexicon.getDefaultLexicon();
    NLGFactory factory = new NLGFactory(lexicon);
    Realiser realiser = new Realiser(lexicon);
    String result;


    public static void main(String [] args) {

        String[] testStrings;
        if (args.length > 0) {
            testStrings = args;
        } else {
            testStrings = new String[]{
                "div.featured a",
                "div.video-summary-data a[href^=/video]",
                "p.introduction::text",
                "div#videobox h3",
                ".watch-view-count",
                ".form_box input:checked"
            };
        }

        for (int i = 0; i < testStrings.length; i++) {
            String string = testStrings[i];
            CssExplainer explainer = new CssExplainer();
            System.out.println(explainer.explain(string));
        }

    }

    public String explain(String selector) {

        ANTLRInputStream input = new ANTLRInputStream(selector);
        CssLexer lexer = new CssLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        CssParser parser = new CssParser(tokens);
        ParseTree tree = parser.selector();
        ParseTreeWalker walker = new ParseTreeWalker();
        walker.walk(this, tree);
        return this.result;

    }

    public void exitSelector(CssParser.SelectorContext ctx) {

        SPhraseSpec sentence = factory.createClause();
        NPPhraseSpec noun = factory.createNounPhrase("selector");
        noun.setDeterminer("the");
        noun.addPostModifier("'" + ctx.getText() + "'");
        sentence.setSubject(noun);
        sentence.setVerb("choose");
        sentence.setComplement(phrases.get(ctx.node()));
        result = realiser.realiseSentence(sentence);

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
            else if (tag.equals("img")) string = "image";
            else if (tag.equals("pre")) string = "preformatted text";
            else string = tag;
            return factory.createNounPhrase(string);
        }

    }

    public NPPhraseSpec getPropertyNoun(String prop) {
        return factory.createNounPhrase(prop);
    }

    public String getPseudoclassAdjective(String pseudoclassName) {
        List<String> adjList = (List<String>) Arrays.asList(
                "checked", "hidden", "visible", "enabled", "active", "empty", "visited");
        if (adjList.contains(pseudoclassName)) return pseudoclassName;
        else if (pseudoclassName.equals("hover")) return "hovered-over";
        else if (pseudoclassName.equals("focus")) return "in-focus";
        return null;
    }

    public void exitNode(CssParser.NodeContext ctx) {

        /* Prepare description of tag */
        NPPhraseSpec tagNoun;
        if (ctx.element() != null) {
            String tag = ctx.element().IDENT().getText();
            tagNoun = getTagNoun(tag);
        } else {
            tagNoun = factory.createNounPhrase("element");
        }

        if (ctx.qualifier() != null) {
            CssParser.QualifierContext qualifier = ctx.qualifier();
            if (qualifier.ident() != null) {
                tagNoun.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR);
                tagNoun.setDeterminer("a");
                tagNoun.addPostModifier("with the ID '" + qualifier.ident().IDENT().getText() + "'");
            } else if (qualifier.klazz() != null) {
                tagNoun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
                tagNoun.addPostModifier("of class '" + qualifier.klazz().IDENT().getText() + "'");
            }
        } else {
            tagNoun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL);
        }

        if (ctx.pseudoclass() != null) {
            String pseudoclassName = ctx.pseudoclass().IDENT().toString();
            String adjective = getPseudoclassAdjective(pseudoclassName);
            if (adjective != null) tagNoun.addPreModifier(adjective);
            else {
                String pcGenericMod = "";
                if (ctx.qualifier() != null) pcGenericMod = "and ";
                else pcGenericMod = "with ";
                pcGenericMod += "pseudoclass " + pseudoclassName;
                tagNoun.addPostModifier(pcGenericMod);
            }
        }

        /* Choose the noun of the node as the prop of the node, if it exists, otherwise the tag itself */
        NPPhraseSpec nodeNoun;
        if (ctx.prop() == null) {
            nodeNoun = tagNoun;
        } else {
            String prop = ctx.prop().IDENT().getText();
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