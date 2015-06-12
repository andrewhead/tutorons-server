This is the repository for research and development on Tutorons.
Tutorons are routines that generate context-relevant micro-explanations

# Dependencies

## System dependencies

To develop on OSX:

0. brew install gettext

Then set your system path (for example, in ~/.bash\_profile)

	export PATH=$PATH:/usr/local/opt/gettext/bin

## Python dependencies

To fetch the Python dependencies for this project, pip install using the
requirements file in the 'files' directory for the
Ansible 'webserver' role in the launch/ directory.

## Java dependencies

Look at the javadeps variable in launch/host\_vars/tutorons.com.
You should download all of these files from the S3 tutorons bucket into
the deps/ folder.

## Compiling source dependencies

This project includes some source code from other open source projects that needs
to be compiled before running the server:

0. cd deps/wget
0. git submodule init && git submodule update
0. ./bootstrap
0. ./configure --with-ssl=openssl
0. make
