domain: tutorons.com
localport: 8002
appname: tutorons
repo: https://github.com/andrewhead/Tutorons.git
djdir: "{{ src }}"
awsbucket: tutorons
djkey: tutorons.key
logfile: /var/log/tutorons.log
staticfiles: yes
javadeps:
- englishPCFG.ser.gz
- stanford-parser-3.4-javadoc.jar
- stanford-parser-3.4-models.jar
- stanford-parser-3.4-sources.jar
- stanford-parser.jar
- py4j-0.8.2.jar
- simplenlg-v4.4.2.jar
- antlr-4.5-complete.jar
- css-explainer-0.1.jar
processes:
- css-explainer
systempkgs:
- default-jre
- libssl-dev # to compile wget
- libxml2-dev # to download PyQuery
- libxslt-dev # to download PyQuery
- autoconf
scripts:
- compile-wget
