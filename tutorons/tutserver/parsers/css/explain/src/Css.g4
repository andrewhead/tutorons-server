grammar Css;


/* Grammar */
selector : node ;

node      : selection prop? attr? (SPACE node)? '\n'?;
selection : element? qualifier |
            element qualifier? ;
element : IDENT;

qualifier : '.' klazz
          | '#' ident ;
klazz : IDENT ;
ident : IDENT ;

prop : '::' IDENT;

attr   : '[' attrname rel attrvalue ']';
attrname  : IDENT;
rel       : '=' |
            '^=' ;
attrvalue : IDENT |
            VALUE;


/* Lexicon */
IDENT : IDCHAR+ ;
VALUE : '\''? ( IDCHAR | '/' )+ '\''? ;
IDCHAR  : [_a-zA-Z0-9-] ;
SPACE   : [ ]+;