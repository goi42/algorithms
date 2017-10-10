from ROOT import TCut
class bfch: #abstract base class for branch and fch classes
    def __init__(self):
        self.c = [] #cuts to be applied
    def add_cut(self,*args,**kwargs):
        if isinstance(args[0],cut):
            if len(args)==1 and len(kwargs)==0:
                self.c.append(*args)
            elif len(args)==2 and isinstance(args[1],str):
                self.add_cut(args[0].cut,args[1])
            elif all(isinstance(x, cut) for x in args):
                self.c.extend(args)
            else:
                raise TypeError
        elif all(isinstance(x, list) for x in args):
            for ar in args:
                if all(isinstance(x, cut) for x in ar):
                    self.c.extend(ar)
                elif all(isinstance(x, (str,TCut)) for x in ar):
                    for ct in ar:
                        self.add_cut(ct)
                else:
                    raise TypeError
        else:
            self.c.append(cut(*args,**kwargs))
