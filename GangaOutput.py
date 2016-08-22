import os, sys
jid = sys.argv[1]
# jid = 317
j = jobs(jid)
base_path = '/afs/cern.ch/user/m/mwilkins/EOS/lhcb/user/m/mwilkins/ganga/outputfiles/'
s = 'Job ID = ' + repr(jid)
print s

for sj in j.subjobs:
   if sj.status != 'completed': continue
   # s = 'On subjob ' + repr(sj)
   # if (sj.id == 4 or sj.id == 46 or sj.id == 50 or sj.id == 54 or sj.id == 74 or sj.id == 97 or sj.id == 105 or sj.id == 113):
   # print s
   for f in sj.outputfiles.get(DiracFile):
      whole_path = os.path.join(base_path, sj.fqid)
      if not os.path.exists(whole_path):
         os.makedirs(whole_path)
         f.localDir = whole_path
         f.get()
