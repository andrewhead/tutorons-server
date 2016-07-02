# CSS Parser

The grammar for the language is defined in `Css.g4`.
The rest of the `Css` files have been automatically generated.
To re-generate the parser boilerplate from the ANTLR4 grammar:

    java -Xmx500M org.antlr.v4.Tool -Dlanguage=Python2 Css.g4
