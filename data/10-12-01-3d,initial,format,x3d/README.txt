Format proposal, as an application of X3D.

Included are scripts and data to validate:
- DTD validation requires xmllint.

- XSD (XML Schema) validation requires SAXCount, it's part of xerces-c project
  (http://xerces.apache.org/xerces-c/).
  Cheatsheet: if you downloaded binary xerces-c distribution from above URL,
  and you don't want to permanently install it (in /usr/local or such),
  you can instead call in your bash session the lines below:

    SAX_PATH=/home/michalis/installed/xerces-c-3.1.1-x86-linux-gcc-3.4/
    export PATH="${PATH}:${SAX_PATH}bin/"
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${SAX_PATH}lib"
