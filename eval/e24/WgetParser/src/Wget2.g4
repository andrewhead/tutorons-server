grammar Wget2 ;
/* This grammar takes the perspective of consuming whitespace and non-whitespace as the main discriminating factors */

lines  : line ('\n' lines)? EOF ;
line   : WGET (WS chunk)* ;
chunk  : url |
         option |
         eoc ;
url    : nospace;
option : SOPTAS shortassign nospace |
         SOPTAS shortassign '-' |
         SOPTSO |
         LOPTAS assign nospace |
         LOPTSO ;
nospace   : NWS ('=' NWS)* ;
eoc       : WS? BAR after | WS? AMP ;
assign      : WS | '=' ;
shortassign : WS | '=' ;
after     : afterloop* ;
afterloop : NWS | WS | '-' | WGET | SOP | LOP ;

SOPTAS   : '-e' | '-o' | '-a' | '-i' | '-B' | '-t' | '-O' | '-T' | '-w' | '-Q' | '-P' | '-U' | '-l' | '-A' | '-R' | '-D' | '-I' | '-X' ;
SOPTSO   : '-V' | '-h' | '-b' | '-d' | '-q' | '-v' | '-rc' | '-nv' | '-F' | '-nc' | '-c' | '-N' | '-S' | '-4' | '-6' | '-nd' | '-x' | '-nH' | '-E' | '-r' | '-k' | '-K' | '-m' | '-p' | '-H' | '-L' | '-np';
LOPTSO   :
'--html-extension' |
'--timestamp' |
'--version'  |
'--help' |
'--background' |
'--debug' |
'--quiet' |
'--verbose' |
'--no-verbose' |
'--force-html' |
'--no-clobber' |
'--continue' |
'--timestamping' |
'--no-use-server-timestamps' |
'--server-response' |
'--spider' |
'--random-wait' |
'--no-proxy' |
'--no-dns-cache' |
'--inet4-only' |
'--inet6-only' |
'--retry-connrefused' |
'--ask-password' |
'--no-iri' |
'--unlink' |
'--no-directories' |
'--force-directories' |
'--no-host-directories' |
'--protocol-directories' |
'--adjust-extension' |
'--no-http-keep-alive' |
'--no-cache' |
'--no-cookies' |
'--keep-session-cookies' |
'--ignore-length' |
'--save-headers' |
'--content-disposition' |
'--content-on-error' |
'--trust-server-names' |
'--auth-no-challenge' |
'--https-only' |
'--no-check-certificate' |
'--warc-cdx' |
'--no-warc-compression' |
'--no-warc-digests' |
'--no-warc-keep-log' |
'--no-remove-listing' |
'--no-glob' |
'--no-passive-ftp' |
'--preserve-permissions' |
'--retr-symlinks' |
'--recursive' |
'--delete-after' |
'--convert-links' |
'--backup-converted' |
'--mirror' |
'--page-requisites' |
'--strict-comments' |
'--follow-ftp' |
'--ignore-case' |
'--span-hosts' |
'--relative' |
'--no-parent' ;
LOPTAS   :
'--cookies' |
'--accept' |
'--cut-dirs' |
'--save-cookies' |
'--reject' |
'--output-file' |
'--append-output' |
'--report-speed' |
'--input-file' |
'--base' |
'--config' |
'--bind-address' |
'--tries' |
'--output-document' |
'--backups' |
'--progress' |
'--timeout' |
'--dns-timeout' |
'--connect-timeout' |
'--read-timeout' |
'--limit-rate' |
'--wait' |
'--waitretry' |
'--quota' |
'--restrict-file-names' |
'--prefer-family' |
'--user' |
'--password' |
'--local-encoding' |
'--remote-encoding' |
'--cut-dirs' |
'--directory-prefix' |
'--default-page' |
'--http-user' |
'--http-password' |
'--header' |
'--max-redirect' |
'--proxy-user' |
'--proxy-password' |
'--referer' |
'--user-agent' |
'--post-data' |
'--post-file' |
'--method' |
'--body-data' |
'--body-file' |
'--secure-protocol' |
'--certificate' |
'--certificate-type' |
'--private-key' |
'--private-key-type' |
'--ca-certificate' |
'--ca-directory' |
'--random-file' |
'--egd-file' |
'--warc-file' |
'--warc-header' |
'--warc-max-size' |
'--warc-dedup' |
'--warc-tempdir' |
'--ftp-user' |
'--ftp-password' |
'--level' |
'--domains' |
'--follow-tags' |
'--ignore-tags' |
'--include-directories' |
'--exclude-directories' |
'--load-cookies';

AMP  : '&';
BAR  : '|';
WGET : 'wget' ;
WS   : [ \s\t]+ ;
NWS  : [a-zA-Z0-9~<>'"\[\]*?,./:&*%+@#!;(){}\^_][a-zA-Z0-9~<>'"\[\]*?,./:&*%+@#!;(){}\^_-]* ;
SOP  : '-' [A-Za-z]+ ;
LOP  : '--' [A-Za-z0-9_-] ;