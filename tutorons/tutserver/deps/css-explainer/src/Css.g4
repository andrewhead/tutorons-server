grammar Css;


/* Grammar */
selector : node ;

node      : selection property? attr? (SPACE node)?;
selection : element? qualifier |
            element qualifier? ;
element : IDENT;

qualifier : '.' klazz
          | '#' id ;
klazz : IDENT ;
id : IDENT ;

property : '::' IDENT;

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