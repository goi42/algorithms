#! /bin/tcsh -f                                                                                                            
#$ -S /bin/tcsh                                                                                                            
#$ -cwd                                                                                                                    

foreach x (`seq 0 1 856`)
set filename = /tmp/mwilkins/412.${x}/2016_Data.root
if ( !(-e ${filename}) ) then
echo $x
endif
end
