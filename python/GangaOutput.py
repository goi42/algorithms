import os, sys
jid = sys.argv[1]
# jid = 317
j = jobs(jid)
base_path = '/tmp/mwilkins/'
s = 'Job ID = ' + repr(jid) + ', ' + j.name
print s

# f = j.outputfiles.get(DiracFile)
# whole_path = os.path.join(base_path, j.fqid)
# if not os.path.exists(whole_path):
#    os.makedirs(whole_path)
#    f.localDir = whole_path
#    f.get()


for sj in j.subjobs:
  if sj.status != 'completed': continue
  s = 'On ' + repr(sj)
  # if (sj.id == 0):
  print s
  for f in sj.outputfiles.get(DiracFile):
    whole_path = os.path.join(base_path, sj.fqid)
    if not os.path.exists(whole_path):
      os.makedirs(whole_path)
      f.localDir = whole_path
      f.get()
        