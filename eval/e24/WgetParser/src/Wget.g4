grammar Wget ;

lines  : line ('\n' lines)? ;
line   : WGET option*  WS url option* (WS '|' after)? ;
url    : URL | '"' URL '"' | '\'' URL '\'' ;
option : ONEDASH SOPTAS ONEDASH |
         ONEDASH SOPTSO |
         ONEDASH SOPTAS assign optvalue |
         TWODASH LOPTAS assign optvalue |
         TWODASH LOPTSO ;
         // ONEDASH SOPTAS NAME |
optvalue  : longvalue | '"' longvalue '"' | '\'' longvalue '\'' ;
longvalue : NAME ('=' longvalue)? ;
assign    : WS | EQUALS ;
after     : afterloop* ;
afterloop : NAME | WS | URL | WGET | ONEDASH | ASTERISK | '|' | SOPTAS | SOPTSO;

SOPTAS   : 'e' | 'o' | 'a' | 'i' | 'B' | 't' | OH | 'T' | 'w' | 'Q' | 'P' | 'U' | 'l' | 'A' | 'R' | 'D' | 'I' | 'X' ;
SOPTSO   : 'V' | 'h' | 'b' | 'd' | 'q' | 'v' | 'rc' | 'nv' | 'F' | 'nc' | 'c' | 'N' | 'S' | '4' | '6' | 'nd' | 'x' | 'nH' | 'E' | 'r' | 'k' | 'K' | 'm' | 'p' | 'H' | 'L' | 'np';
LOPTSO   :
'timestamp' |
'version'  |
'help' |
'background' |
'debug' |
'quiet' |
'verbose' |
'no-verbose' |
'force-html' |
'no-clobber' |
'continue' |
'timestamping' |
'no-use-server-timestamps' |
'server-response' |
'spider' |
'random-wait' |
'no-proxy' |
'no-dns-cache' |
'inet4-only' |
'inet6-only' |
'retry-connrefused' |
'ask-password' |
'no-iri' |
'unlink' |
'no-directories' |
'force-directories' |
'no-host-directories' |
'protocol-directories' |
'adjust-extension' |
'no-http-keep-alive' |
'no-cache' |
'no-cookies' |
'keep-session-cookies' |
'ignore-length' |
'save-headers' |
'content-disposition' |
'content-on-error' |
'trust-server-names' |
'auth-no-challenge' |
'https-only' |
'no-check-certificate' |
'warc-cdx' |
'no-warc-compression' |
'no-warc-digests' |
'no-warc-keep-log' |
'no-remove-listing' |
'no-glob' |
'no-passive-ftp' |
'preserve-permissions' |
'retr-symlinks' |
'recursive' |
'delete-after' |
'convert-links' |
'backup-converted' |
'mirror' |
'page-requisites' |
'strict-comments' |
'follow-ftp' |
'ignore-case' |
'span-hosts' |
'relative' |
'no-parent' ;
LOPTAS   :
'cut-dirs' |
'save-cookies' |
'reject' |
'output-file' |
'append-output' |
'report-speed' |
'input-file' |
'base' |
'config' |
'bind-address' |
'tries' |
'output-document' |
'backups' |
'progress' |
'timeout' |
'dns-timeout' |
'connect-timeout' |
'read-timeout' |
'limit-rate' |
'wait' |
'waitretry' |
'quota' |
'restrict-file-names' |
'prefer-family' |
'user' |
'password' |
'local-encoding' |
'remote-encoding' |
'cut-dirs' |
'directory-prefix' |
'default-page' |
'http-user' |
'http-password' |
'header' |
'max-redirect' |
'proxy-user' |
'proxy-password' |
'referer' |
'user-agent' |
'post-data' |
'post-file' |
'method' |
'body-data' |
'body-file' |
'secure-protocol' |
'certificate' |
'certificate-type' |
'private-key' |
'private-key-type' |
'ca-certificate' |
'ca-directory' |
'random-file' |
'egd-file' |
'warc-file' |
'warc-header' |
'warc-max-size' |
'warc-dedup' |
'warc-tempdir' |
'ftp-user' |
'ftp-password' |
'level' |
'domains' |
'follow-tags' |
'ignore-tags' |
'include-directories' |
'exclude-directories' |
'load-cookies';

EQUALS     : '=' ;
ASTERISK   : '*' ;
WGET       : 'wget' ;
ONEDASH    : WS '-' ;
TWODASH    : WS '--' ;
NAME       : [a-zA-Z0-9][a-zA-Z0-9&.?/_~*-]* ;
URL        : [a-z]+ '://' [a-zA-Z0-9.:?/=_~-]+ ;
WS         : [ \s\t]+ ;
OH         : 'O' ;
