

from numpy import isin
import random

class LeafNode:
    def __init__(self):
        self.name = ''
    def __str__(self):
        return self.name
class Node:
    def __init__(self):
        self.name = ''
        self.nodes = []
    def randomNode(self, depth):
        pass
    def __str__(self):
        out = '\n'+self.name+' {'
        iscomma = False
        for n in self.nodes:
            if isinstance(n, LeafNode):
                if iscomma:
                    out+=', '
                else:
                    out+='\n'
                out+=n.__str__()
                iscomma = True
            else:
                iscomma = False
                out+=n.__str__()
        return out+'\n}'

class BtnInactive(LeafNode):
    def __init__(self):
        self.name = 'btn-inactive'
class BtnActive(LeafNode):
    def __init__(self):
        self.name = 'btn-active'
class BtnRed(LeafNode):
    def __init__(self):
        self.name = 'btn-red'
class BtnOrange(LeafNode):
    def __init__(self):
        self.name = 'btn-orange'
class BtnYellow(LeafNode):
    def __init__(self):
        self.name = 'btn-yellow'
class BtnGreen(LeafNode):
    def __init__(self):
        self.name = 'btn-green'
class BtnPurple(LeafNode):
    def __init__(self):
        self.name = 'btn-purple'
class BigTitle(LeafNode):
    def __init__(self):
        self.name = 'big-title'
class SmallTitle(LeafNode):
    def __init__(self):
        self.name = 'small-title'
class Text(LeafNode):
    def __init__(self):
        self.name = 'text'

leaf = [BtnRed(),BtnOrange(), BtnYellow(), BtnGreen(), BtnPurple(), BigTitle(), SmallTitle(), Text()]
hleaf = [BtnActive(), BtnInactive()]

nonleaf = []

class Header(Node):
    def __init__(self):
        self.name = 'header'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 6)
        for _ in range(cnt):
            self.nodes.append(hleaf[random.randrange(0, len(hleaf))])

class Row(Node):
    def __init__(self):
        self.name = 'row'
    def randomNode(self, depth):
        self.nodes = []
        p = random.randrange(0, 4)
        for _ in range(nonleaf[p][1]):
            # if random.randrange(1, 3)==1 or depth>2:
            #     self.nodes.append(leaf[random.randrange(0, len(leaf))])
            # else:
            nxt = factoryNonleaf(nonleaf[p][1])
            nxt.randomNode(depth+1)
            self.nodes.append(nxt)

def factoryNonleaf(i: int):
    if i==1:
        return Single()
    elif i==2:
        return Double()
    elif i==3:
        return Triple()
    elif i==4:
        return Quadruple()

class Single(Node):
    def __init__(self):
        self.name = 'single'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 3)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

class Double(Node):
    def __init__(self):
        self.name = 'double'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 3)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

class Triple(Node):
    def __init__(self):
        self.name = 'triple'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 3)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

class Quadruple(Node):
    def __init__(self):
        self.name = 'quadruple'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 3)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

nonleaf = [('single',1), ('double',2), ('triple',3), ('quadruple',4)]

class Dsl():
    def getDsl(self):
        h = Header()
        h.randomNode(0)
        out = h.__str__()
        for _ in range(random.randrange(1, 4)):
            r = Row()
            r.randomNode(0)
            out += r.__str__()
        return out


if __name__=='__main__':
    d = Dsl()
    print(d.getDsl())