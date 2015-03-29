from optparse import OptionParser
parser = OptionParser(conflict_handler="resolve")

# two default functions for options with zero and one arguments, respectively
def default_boolean(option, opt_str, value, parser):
	if str(option)==str(opt_str):
		print " * The option %s is present. We don't know much about it yet. It does not take any arguments"%opt_str;
	else:
		print " * The option %s is present (alternate forms: %s). We don't know much about it yet. It does not take any arguments"%(opt_str,option);

def default_string(option, opt_str, value, parser):
	if str(option)==str(opt_str):
		print " * The option %s is present with its argument %s. We don't know much about it yet. "%(opt_str,value);
	else:
		print " * The option %s is present with its argument %s (alternate forms: %s). We don't know much about it yet. "%(opt_str,value,option);

# here come all the options
parser.add_option("-V","--version",action="store_true")
parser.add_option("-h","--help",action="store_true")
parser.add_option("-b","--background",action="store_true")
parser.add_option("-e","--execute")

def output_file(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print(" * The option %s logs all messages to the file named '%s'."%(opt_str,value))
	print("   The messages are normally reported to standard error.")
parser.add_option("-o","--output-file",action="callback",callback=output_file,type="string")

parser.add_option("-a","--append-output")
parser.add_option("-d","--debug",action="store_true")
parser.add_option("-q","--quiet",action="store_true")
parser.add_option("-v","--verbose",action="store_true")
parser.add_option("--nv", "--no-verbose", dest="verbose", action="store_false") #nonstandard
parser.add_option("--report-speed")

def input_file(option,opt_str,value,parser):
	#setattr(parser.values, option.dest, value)
	if value is '-':
		print(" * The option %s with argument %s  reads URLs from the standard input. (Use './-'' to read from a file literally named '-'.)"%(opt_str,value))
	else:
		print(" * The option %s reads URLs from a local or external file named '%s'."%(opt_str,value))
	print("   If this function is used, no URLs need be present on the command line.") 
parser.add_option("-i","--input-file",action="callback",callback=input_file,type="string")
parser.add_option("-F","--force-html",action="callback",callback=default_boolean,dest="force_html")
parser.add_option("-B","--base")
parser.add_option("--bind-address")

def tries(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print " * The option %s sets the number of download attempts to %s."%(opt_str,value)
	print '''   Specify 0 or 'inf' for infinite retrying. The default is to retry 20 times, with the exception of fatal errors like "connection refused" or "not found" (404), which are not retried.'''
parser.add_option("-t","--tries",action="callback",callback=tries, type="string")


def output_document(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	if value is '-':
		print " * The option %s with argument %s  concatenates all documents together and prints them to standard output. (Use './-' to print to  a file literally named '-'.)"%(opt_str,value)
	else:
		print " * The option %s concatenates all documents together and writes them to file '%s'"%(opt_str,value)
parser.add_option("-O","--output-document", action="callback", callback=output_document, type="string")
parser.add_option("--nc","--no-clobber",action="callback",callback=default_boolean,dest="no_clobber")
parser.add_option("--backups")
parser.add_option("-c","--continue",action="store_true")
parser.add_option("--start-pos")
parser.add_option("--progress")
parser.add_option("--show-progress",action="store_true")
parser.add_option("-N","--timestamping",action="store_true")
parser.add_option("--no-use-server-timestamps",action="store_true")
parser.add_option("-S","--server-response",action="callback",callback=default_boolean,dest="server_response")
parser.add_option("--spider",action="store_true")
parser.add_option("-T","--timeout")
parser.add_option("--dns-timeout")
parser.add_option("--connect-timeout")
parser.add_option("--read-timeout")
parser.add_option("--limit-rate")
parser.add_option("-w","--wait")
parser.add_option("--waitretry")
parser.add_option("--random-wait",action="store_true")
parser.add_option("--no-proxy",action="store_true")
parser.add_option("-Q","--quota")
parser.add_option("--no-dns-cache",action="store_true")
parser.add_option("--restrict-file-names")
parser.add_option("-4","--inet4-only",action="store_true")
parser.add_option("-6","--inet6-only",action="store_true")
parser.add_option("--prefer-family")
parser.add_option("--retry-connrefused",action="store_true")
parser.add_option("--user")
parser.add_option("--password")
parser.add_option("--ask-password",action="store_true")
parser.add_option("--no-iri",action="store_true")
parser.add_option("--local-encoding")
parser.add_option("--remote-encoding")
parser.add_option("--unlink",action="store_true")

parser.add_option("--nd","--no-directories",dest="no_directories",action="callback",callback=default_boolean)
parser.add_option("-x","--force-directories",action="store_true")
parser.add_option("--nH","--no-host-directories",dest="no_host_directories",action="callback",callback=default_boolean)
parser.add_option("--protocol-directories",action="store_true")
parser.add_option("--cut-dirs")

def directory_prefix(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print''' * The option %s sets directory prefix to '%s'. '''%(opt_str,value)
	print'''   The directory prefix is the directory where all other files and subdirectories will be saved to, i.e. the top of the retrieval tree. The default is '.' (the current directory).'''
parser.add_option("-P","--directory-prefix",action="callback",callback=directory_prefix,type="string")

parser.add_option("--default-page")
parser.add_option("-E","--adjust-extension",action="store_true")
parser.add_option("--http-user")
parser.add_option("--https-password")
parser.add_option("--no-http-keep-alive",action="store_true")
parser.add_option("--no-cache",action="store_true")
parser.add_option("--no-cookies",action="store_true")
parser.add_option("--load-cookies")
parser.add_option("--save-cookies")
parser.add_option("--keep-session-cookies",action="store_true")
parser.add_option("--ignore-length",action="store_true")
parser.add_option("--header")
parser.add_option("--max-redirect")
parser.add_option("--proxy-user")
parser.add_option("--proxy-password")
parser.add_option("--referer")
parser.add_option("--save-headers",action="store_true")
parser.add_option("-U","--user-agent")
parser.add_option("--post-data")
parser.add_option("--post-file")
parser.add_option("--method")
parser.add_option("--body-data")
parser.add_option("--body-file")
parser.add_option("--content-disposition",action="store_true")
parser.add_option("--content-on-error",action="store_true")
parser.add_option("--trust-server-names",action="store_true")
parser.add_option("--auth-no-challenge",action="store_true")
#skipped section 2.8 - http://www.gnu.org/software/wget/manual/html_node/HTTPS-_0028SSL_002fTLS_0029-Options.html#HTTPS-_0028SSL_002fTLS_0029-Options
#skipped section 2.9
def recursive(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print ''' * The option %s turns on recursive retrieving. See Recursive Download, for more details. The default maximum depth is 5. Change this with -l or --level.'''%opt_str
parser.add_option("-r","--recursive",action="callback",callback=recursive,dest="recursive")
parser.add_option("-l","--level",action="callback",callback=default_string,type="string")
parser.add_option("--delete-after",action="store_true")

def convert_links(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print ''' * The option %s converts the links in the document to make them suitable for local viewing, after download is complete.'''%opt_str
parser.add_option("-k","--convert-links",action="callback",callback=convert_links,dest="convert_links")

parser.add_option("-K","--backup-converted",action="store_true")
parser.add_option("-m","--mirror",action="store_true")

def page_requisites(option, opt_str, value, parser):
	#setattr(parser.values, option.dest, value)
	print ''' * The option %s causes Wget to download all the files that are necessary to properly display a given HTML page. This includes such things as inlined images, sounds, and referenced stylesheets.'''%opt_str
parser.add_option("-p","--page-requisites",action="callback",callback=page_requisites,dest="page_requisites")
parser.add_option("--strict-comments",action="store_true")

parser.add_option("-A","--accept",action="callback",callback=default_string,type="string"),
parser.add_option("-R","--reject")
parser.add_option("--accept-regex")
parser.add_option("--reject-regex")
parser.add_option("--regex-type")
parser.add_option("-D","--domains")
parser.add_option("--exclude-domains")
parser.add_option("--follow-ftp",action="store_true")
parser.add_option("--follow-tags")
parser.add_option("--ignore-tags")
parser.add_option("--ignore-case",action="store_true")
parser.add_option("-H","--span-hosts",action="store_true")
parser.add_option("-L","--relative",action="store_true")
parser.add_option("-I","--include-directories")
parser.add_option("-X","--exclude-directories")
parser.add_option("--np","--no-parent",dest="no_parent",action="callback",callback=default_boolean)

# optparse doesn't like '-XY' options (single dash followed by multiple letters)
# so we'll find and replace them with a double-dash version later
replacements = [(' -nv ',' --nv '),(' -nc ',' --nc '),(' -nd ',' --nd '),(' -nH ',' --nH '),(' -np ',' --np ')]


# test code below - try to parse and describe a number of wget examples from the web

tests = ['wget http://fly.srk.fer.hr/',
'wget --tries=45 http://fly.srk.fer.hr/jpg/flyweb.jpg',
'wget -t 45 -o log http://fly.srk.fer.hr/jpg/flyweb.jpg &',
'wget ftp://gnjilux.srk.fer.hr/welcome.msg',
'wget ftp://ftp.gnu.org/pub/gnu/',
'wget -i file',
'wget -r http://www.gnu.org/ -o gnulog',
'wget --convert-links -r http://www.gnu.org/ -o gnulog',
'wget -p --convert-links http://www.server.com/dir/page.html',
'''wget -p --convert-links -nH -nd -Pdownload \
     http://www.server.com/dir/page.html''',
'wget -S http://www.lycos.com/',
'wget --save-headers http://www.lycos.com/',
'wget -r -l2 -P/tmp ftp://wuarchive.wustl.edu/',
'wget -r -l1 --no-parent -A.gif http://www.server.com/dir/',
'wget -nc -r http://www.gnu.org/',
'wget ftp://hniksic:mypassword@unix.server.com/.emacs',
'wget -O - http://jagor.srce.hr/ http://www.srce.hr/',
'wget -O - http://cool.list.com/ | wget --force-html -i -']
for t in tests:
	print t
	for (old,new) in replacements:
		t=t.replace(old,new)		
	(options,args) = parser.parse_args(t.split()) # actual parsing happens here

	# loop over options that were set and that we haven't described yet
	# should be replaced with default_callbacks later.
	interesting_options = [(k,v) for (k,v) in options.__dict__.iteritems() if v is not None]
	for (k,v) in interesting_options:
		if v is True:
			print " * Option %s is present but we don't have a description for it yet. We do know that it takes no arguments. "%k
		else:
			print " * Option %s is present and takes argument %s. We don't have a description for it yet."%(k,v)
	#print({k:v for (k,v) in options.__dict__.iteritems() if v is not None})
	#print(args)

	# the leftover "positional" args should all be URLs (args[0] is always 'wget')
	if(len(args[1:])>0):
		print(" * The following URLs will be retrieved: %s"%args[1:])
	print("========")
