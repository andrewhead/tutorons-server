grammar Css;


/* Grammar */
selector : node ;

node      : element? qualifier? prop? pseudoclass? attr? (SPACE node)? '\n'?;
element : IDENT;

qualifier : '.' klazz
          | '#' ident ;
klazz : IDENT ;
ident : IDENT ;

pseudoclass : ':' IDENT;
prop        : '::' IDENT;

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