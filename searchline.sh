#!/bin/bash

files='/afs/cern.ch/user/m/mwilkins/cmtuser/DaVinci_v37r2p4/Phys/StrippingSelections/tests/data/Reco15a_Run164668.xml /afs/cern.ch/user/m/mwilkins/b_b-bar_cross-section/GEC/teststripping/DV_v37r2p4/test/makedst/trymoreLFNs/pool_xml_catalog.xml'
for file in $files; do ./rr.sh $file | grep '.*rdst.*' | grep -v '.*lfn name=.*' | grep -c '.*root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/freezer/lhcb/LHCb/Collision15/RDST/00048237/0000/.*'; done