#! /bin/tcsh -f                                                                                                            
#$ -S /bin/tcsh                                                                                                            
#$ -cwd                                                                                                                    

foreach x (`seq 0 1 114`)
set filename = /tmp/mwilkins/336.${x}/DVNtuples.root
if ( !(-e ${filename}) ) then
echo $x
endif
end
