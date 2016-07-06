grammar Css;

// This is based on the grammar defined in the W3C Recommendation
// at https://www.w3.org/TR/css3-selectors/#w3cselgrammar.
// 
// We make the following modifications to the specs:
// 1. We ignore the "nonascii" fragment as it wasn't clear to
//    the author at the time of writing this how to specify
//    non-ASCII characters with ANTLR.
// 2. We left out comments
// 3. We do not look for unicode letters for the :not( pseudoclass

selectors_group : selector ( COMMA SPACE* selector )*
  ;

selector :
  simple_selector_sequence
  ( combinator simple_selector_sequence ) *
  ;

combinator :
  PLUS SPACE* |
  GREATER SPACE* |
  TILDE SPACE* |
  SPACE+
  ;

simple_selector_sequence :
  (type_selector | universal)
  (hash_ | class_ | attribute | pseudo | negation)*
  ;

type_selector : namespace_prefix? element_name
  ;

namespace_prefix : (IDENTIFIER | STAR)? BAR
  ;

element_name : IDENTIFIER
  ;

universal :
  namespace_prefix? STAR |
  ;

hash_ : HASH
  ;

class_ : DOT IDENTIFIER
  ;

attribute :
  LEFT_BRACKET SPACE* namespace_prefix? IDENTIFIER SPACE* ((
    PREFIXMATCH |
    SUFFIXMATCH |
    SUBSTRINGMATCH |
    EQUALS |
    INCLUDES |
    DASHMATCH
  ) SPACE* (
    IDENTIFIER |
    STRING
  ) SPACE*)? RIGHT_BRACKET
  ;

pseudo :
  COLON COLON? (
    IDENTIFIER |
    functional_pseudo
  )
  ;

functional_pseudo : FUNCTION SPACE* expression RIGHT_PARENTHESIS
  ;

expression :
  ((
    PLUS |
    '-' |
    DIMENSION |
    NUMBER |
    STRING |
    IDENTIFIER
  ) SPACE*)+
  ;

negation :
  NOT SPACE* negation_argument SPACE* RIGHT_PARENTHESIS
  ;

negation_argument:
  type_selector |
  universal |
  hash_ |
  class_ |
  attribute
  ;

fragment
Name : Nmchar+
  ;

fragment
Identifier : '-'? Nmstart Nmchar*
  ;

fragment
Nmstart :
  Alpha |
  '_' |
  Escape
  ;

fragment
Nmchar :
  Nmstart |
  Digit |
  '-'
  ;

fragment
Alpha :
  'A'..'Z' |
  'a'..'z'
  ;

fragment
Digit :
  '0'..'9'
  ;

fragment
Escape :
  '\\' (
  ~('\r' | '\n' | '\f' | '0'..'9' | 'a'..'f' | 'A'..'F')
  ) |
  Unicode
  ;

fragment
Unicode :
  '\\'
  HexDigit HexDigit? HexDigit? HexDigit? HexDigit? HexDigit? (
  '\r\n' |
  ' ' |
  '\n' |
  '\r' |
  '\t' |
  '\f'
  )?
  ;

fragment
HexDigit :
  'A'..'F' |
  'a'..'f' |
  '0'..'9'
  ;

fragment
Number :
  Digit+ |
  Digit* '.' Digit+
  ;

fragment
SingleQuoteString :
  '\'' (
    ~('\n' | '\r' | '\f' | '\\' | '\'') |
    ('\\' Newline) |
    Escape
  )*
  '\''
  ;

fragment
DoubleQuoteString :
  '"' (
    ~('\n' | '\r' | '\f' | '\\' | '"') |
    ('\\' Newline) |
    Escape
  )*
  '"'
  ;

fragment
Newline :
  '\n' |
  '\r\n' |
  '\r' |
  '\f' ;

fragment
OptionalSpace :
  (
    ' ' |
    '\t' |
    '\r' |
    '\n' |
    '\f'
  )*
  ;

// TOKENS
SPACE :
  (
    ' ' |
    '\t' |
    '\r' |
    '\n' |
    '\f'
  )+
  ;

INCLUDES : '~='
  ;

DASHMATCH : '|='
  ;

PREFIXMATCH : '^='
  ;

SUFFIXMATCH : '$='
  ;

SUBSTRINGMATCH : '*='
  ;

IDENTIFIER : Identifier
  ;

STRING :
  SingleQuoteString | 
  DoubleQuoteString
  ;

FUNCTION : Identifier '('
  ;

NUMBER : Number
  ;

PLUS : OptionalSpace '+'
  ;

GREATER : OptionalSpace '>'
  ;

COMMA : OptionalSpace ','
  ;

TILDE : OptionalSpace '~'
  ;

NOT : COLON
  ('N' | 'n')
  ('O' | 'o')
  ('T' | 't')
  '('
  ;

ATKEYWORD : '@' Identifier
  ;

PERCENTAGE : Number '%'
  ;

DIMENSION : Number Identifier
  ;

COLON : ':'
  ;

STAR : '*'
  ;

DASH : '-'
  ;

EQUALS : '='
  ;

BAR : '|'
  ;

DOT : '.'
  ;

LEFT_BRACKET : '['
  ;

RIGHT_BRACKET : ']'
  ;

RIGHT_PARENTHESIS : ')'
  ;

HASH : '#' Name
  ;
