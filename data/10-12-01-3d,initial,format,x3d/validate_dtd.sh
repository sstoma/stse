#!/bin/bash
set -eu

dovalidate ()
{
  echo '--- Validating ' "$1"
  sed "$1" -e 's|http://www.web3d.org/specifications/x3d-3.2.dtd|file://'`pwd`'/x3d-3.2.dtd|' > validate_dtd-tmp.x3d
  set +e
  xmllint --noout --xinclude --postvalid --noent validate_dtd-tmp.x3d 2>&1 | grep --invert-match 'Content model of ProtoBody is not determinist'
  set -e
  rm -f validate_dtd-tmp.x3d
}

dovalidate initial.x3d
dovalidate initial_2d.x3d
