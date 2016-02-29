import os, sys
jid = sys.argv[1]
# jid = 317
j = jobs(jid)
base_path = '/tmp/mwilkins/'
s = 'Job ID = ' + repr(jid)
print s

for sj in j.subjobs:
   if sj.status != 'completed': continue
   s = 'On subjob ' + repr(sj)
   for f in sj.outputfiles.get(DiracFile):
      #if (sj.id == 21 or sj.id == 57 or sj.id == 61 or sj.id == 48 or sj.id ==386):
      whole_path = os.path.join(base_path, sj.fqid)
      if not os.path.exists(whole_path):
         os.makedirs(whole_path)
      f.localDir = whole_path
      f.get()
