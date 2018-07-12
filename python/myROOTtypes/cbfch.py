class cbfch:  # abstract base class for cut, branch, and fch classes
    def __init__(self, linecolor=None, fillcolor=None, fillstyle=None):
        self.linecolor = linecolor
        self.fillcolor = fillcolor
        self.fillstyle = fillstyle
