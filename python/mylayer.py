class mylayer:
    def __init__(self,element):
        if len(element) == 0:
            raise IndexError('can only create layers from not-empty lists')
        self.name=element[0].__class__.__name__ #this is the type of layer
        self.element=element #element is a list of objects
        self.nL= len(self.element)
        self.Li = 0 #index indicating which element/comparison of the layer we are on should be iterated in code
        self.nLec=0 #should be set = element.size() or comparison.size()
        self.plL = 1 #products of things in lower levels should be calculated in code
        self.plLx = 1 #products of things in lower levels that are not branches or cuts
        self.plLec = 1 #products of things in lower levels using nLec instead of nL
        self.plLecx = 1
        self.compared = False #indicates whether this layer is to be drawn on a canvas with other layers
        self.comparison = {}
    def add_element(self,temp):
        self.element.append(temp)
        self.nL = len(self.element)
        self.name = temp.__class__.__name__
    def add_comparison(self,key,value):
        self.comparison[key]=value
    def add_e_c(self,key,value):
        self.add_element(key)
        self.add_element(value)
        self.add_comparison(key,value)
