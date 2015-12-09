#! /bin/tcsh -f                                                                                                            
#$ -S /bin/tcsh                                                                                                            
#$ -cwd                                                                                                                    

foreach x (`seq 0 1 33`)
set filename = /tmp/mwilkins/263.${x}/DVNtuples.root
if ( !(-e ${filename}) ) then
echo $x
endif
end
