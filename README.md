The Tutorons server listens for HTML webpages, scans them for explainable code, and generates rich HTML-formatted explanations of the code that can be viewed in the browser.
The server can be extended to detect and explain code of many languages.
The current server detects and explains code from three languages that often appear embedded in tutorial pages: `wget` command lines, CSS selectors, and regular expressions.

# Installing Project Dependencies

Tutorons is a unique project in that it leverages parsers from many languages to produce different parse structures that will be automatically explained.  Therefore, the Python code has to interface with both C code and Java.  This means you'll have to go further than `pip` installation to get set up, if you want to work with the full suite of example Tutorons (for wget, CSS selectors, and regular expressions).

## OSX-specific instructions

Download dependencies via HomeBrew

    brew install gettext

Then update your system path (for example, in `~/.bash\_profile`)

    export PATH=$PATH:/usr/local/opt/gettext/bin

## Installing Python dependencies

    pip install -r launch/roles/webserver/files/tutorons-reqs.txt

It is recommended that you install these into a virtualenv:

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r launch/roles/webserver/files/tutorons-reqs.txt

Remember that if you use a virtual environment, you will have to run `source venv/bin/activate` every time that you want to run the server.

## Java dependencies

Fetch all `.jar` files listed in the `external_deps` variable in `launch/host_vars/tutorons.com`.  The latest version of these dependencies used on the Tutorons server can be found in the S3 `tutorons` bucket.  Download each of these files into the `deps` folder.

## Compile source code for command line utilities

Before the next steps, run `git submodule init && git submodule update` from the main project directory.
The following compilation steps work for OSX.
For Ubuntu-specific compilation rules, see the `launch/roles/webserver/templats/compile-*.j2` files.

### wget

    cd deps/wget
    ./bootstrap
    ./configure --with-ssl=openssl
    make

### sed

    cd deps/sed
    ./bootstrap
    ./configure
    make

### grep

    ACLOCAL_path=/usr/local/share/aclocal/:$ACLOCAL_PATH cd deps/sed
    ./bootstrap
    ./configure
    WERROR_CFLAGS= make -e

# Contributing

## How to contribute new code

1. Create a new branch for doing your work: `git checkout -b <branchname>`
2. Do your local work (including unit tests) and commit
3. Run the test suite to make sure everything still passes
4. Push your branch
4. Submit a pull request to merge into master ([see here](https://help.github.com/articles/using-pull-requests/)).  Assign the pull request to someone else on the team who should verify the style and design choices of your code.
6. Respond to any comments you get from reviewers
7. Once your pull request is accepted, merge your pull request into master
8. Check out the master branch and verify that all tests still pass
