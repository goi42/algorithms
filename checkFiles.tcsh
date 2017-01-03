#! /bin/tcsh -f                                                                                                            
#$ -S /bin/tcsh                                                                                                            
#$ -cwd                                                                                                                    

foreach x (`seq 0 1 48`)
set filename = /tmp/mwilkins/374.${x}/LimDVNtuples.root
if ( !(-e ${filename}) ) then
echo $x
endif
end
