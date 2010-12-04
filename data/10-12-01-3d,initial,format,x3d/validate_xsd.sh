#!/bin/bash
set -eu

dovalidate ()
{
  echo '--- Validating ' "$1"
  # Use always local XSD, fixed (for ClipPlane etc.) and in the future
  # validating also STSE extensions.
  # Also, remove DTD (otherwise SAXCount downloads it and reports DTD errors).
  sed "$1" \
    -e 's|http://www.web3d.org/specifications/x3d-3.2.xsd|file://'`pwd`'/x3d-3.2.xsd|' \
    -e 's|<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">||' \
    > validate_xsd-tmp.x3d
  SAXCount -s -v=always -n -f validate_xsd-tmp.x3d
  rm -f validate_xsd-tmp.x3d
}

dovalidate initial.x3d
dovalidate initial_2d.x3d
