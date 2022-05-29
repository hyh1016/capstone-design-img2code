

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
class BtnGreen(LeafNode):
    def __init__(self):
        self.name = 'btn-green'
class BtnOrange(LeafNode):
    def __init__(self):
        self.name = 'btn-orange'
class BtnRed(LeafNode):
    def __init__(self):
        self.name = 'btn-red'
class BigTitle(LeafNode):
    def __init__(self):
        self.name = 'big-title'
class SmallTitle(LeafNode):
    def __init__(self):
        self.name = 'small-title'
class Text(LeafNode):
    def __init__(self):
        self.name = 'text'

leaf = [BtnActive(), BtnInactive(), BtnGreen(), BtnOrange(), BtnRed(), BigTitle(), SmallTitle(), Text()]
nonleaf = []

class Header(Node):
    def __init__(self):
        self.name = 'header'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 10)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

class Row(Node):
    def __init__(self):
        self.name = 'row'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 3)
        for _ in range(cnt):
            # if random.randrange(1, 3)==1 or depth>2:
            #     self.nodes.append(leaf[random.randrange(0, len(leaf))])
            # else:
            nxt = nonleaf[random.randrange(0, len(nonleaf))]
            nxt.randomNode(depth+1)
            self.nodes.append(nxt)

class Single(Node):
    def __init__(self):
        self.name = 'single'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 10)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])
class Double(Node):
    def __init__(self):
        self.name = 'double'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 10)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])
class Quadruple(Node):
    def __init__(self):
        self.name = 'quadruple'
    def randomNode(self, depth):
        self.nodes = []
        cnt = random.randrange(1, 10)
        for _ in range(cnt):
            self.nodes.append(leaf[random.randrange(0, len(leaf))])

nonleaf = [Single(), Double(), Quadruple()]

class Dsl():
    def getDsl(self):
        h = Header()
        h.randomNode(0)
        out = h.__str__()
        for _ in range(random.randrange(0, 5)):
            r = Row()
            r.randomNode(0)
            out += r.__str__()
        return out


if __name__=='__main__':
    d = Dsl()
    print(d.getDsl())