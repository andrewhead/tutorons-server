domain: tutorons.com
localport: 8002
appname: tutorons
repo: https://github.com/andrewhead/Tutorons.git
djdir: "{{ src }}"
publicbucket: tutorons-public
publicdir: tutorons-server-deps
privatebucket: tutorons
djkey: tutorons.key
logfile: /var/log/tutorons.log
staticfiles: yes
external_deps:
- englishPCFG.ser.gz
- stanford-parser-3.4-models.jar
- stanford-parser.jar
- py4j-0.8.2.jar
- simplenlg-v4.4.2.jar
- antlr-4.5-complete.jar
systempkgs:
- default-jre
- libssl-dev  # to compile wget
- libxml2-dev  # to download PyQuery
- libxslt-dev  # to download PyQuery
- autoconf
- unzip
- gettext  # wget
- autopoint  # wget
- flex  # wget
- texinfo  # wget
- pkg-config  # wget
- gperf  # to compile grep
scripts:
- compile-grep
- compile-sed
- compile-wget
containers:
- {"image": "andrewhead/regexper-server", "host_port": 8005, "exposed_port": 8080, "name": "regexper-server"}
- {"image": "andrewhead/regex-svg-server", "host_port": 8006, "exposed_port": 8080, "name": "regex-svg-server"}
subdomains:
- {"subdomain": "regexper", "port": 8005}
- {"subdomain": "regexsvg", "port": 8006}
