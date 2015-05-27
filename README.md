This is the repository for research and development on Tutorons.
Tutorons are routines that generate context-relevant micro-explanations
for code examples programmers find online.  This consists of two
components:

0. Tutorons: routines that generate explanations.  Found in the 
tutorons/tutserver directory.
0. Tutorons Addon: browser addon for Firefox that enables one to query the
Tutorons servers for micro-explanations.

# Dependencies
To install the dependencies for this project, pip install using the
appropriate requirements file in the 'files' directory for the
Ansible 'webserver' role in the launch/ directory.

## Running experiment code
E30.  Stanford Parser jars and englighPCFG.ser.gz in deps/sp/
