#!/bin/bash

files='/afs/cern.ch/user/m/mwilkins/cmtuser/DaVinci_v37r2p4/Phys/StrippingSelections/tests/data/Reco15a_Run164668.xml /afs/cern.ch/user/m/mwilkins/b_b-bar_cross-section/GEC/teststripping/DV_v37r2p4/test/makedst/trymoreLFNs/pool_xml_catalog.xml'
for file in $files; do ./rr.sh $file | grep '.*raw.*' | grep -v '.*lfn name=.*' | grep -c '.*mdf:root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/freezer/lhcb/data/2015/RAW/FULL/LHCb/COLLISION15/164668.*'; done