#!/bin/bash
set -eu

dovalidate ()
{
  echo '--- Validating ' "$1"
  # Use always local DTD, fixed (for ClipPlane etc.) and in the future
  # validating also STSE extensions.
  sed -e 's|http://www.web3d.org/specifications/x3d-3.2.dtd|file://'`pwd`'/x3d-3.2.dtd|' "$1" > validate_dtd-tmp.x3d
  set +e
  xmllint --noout --postvalid validate_dtd-tmp.x3d 2>&1 | grep --invert-match 'Content model of ProtoBody is not determinist'
  set -e
  rm -f validate_dtd-tmp.x3d
}

dovalidate initial.x3d
dovalidate initial_2d.x3d
