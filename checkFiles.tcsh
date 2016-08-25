#! /bin/tcsh -f                                                                                                            
#$ -S /bin/tcsh                                                                                                            
#$ -cwd                                                                                                                    

foreach x (`seq 0 1 359`)
set filename = /afs/cern.ch/user/m/mwilkins/EOS/lhcb/user/m/mwilkins/ganga/outputfiles/354.${x}/LimDVNtuples.root
if ( !(-e ${filename}) ) then
echo $x
endif
end
