from HtmlToPng import *
from MakeHtml import MakeHtml
import RandomDSL
from RandomDSL import *
from posixpath import abspath
import os

path = 'dataGenerator/data/'
def make_dir():
    os.makedirs('./dataGenerator/data/dsl', exist_ok=True)
    os.makedirs('./dataGenerator/data/html', exist_ok=True)
    os.makedirs('./dataGenerator/data/png', exist_ok=True)

def make_data(iter: int):
    rd = Dsl()
    g = HtmlToPng()
    for num in range(iter):
        with open(path+'dsl/'+str(num)+'.gui', 'w') as f:
            f.write(rd.getDsl()[1:])
        
        mh = MakeHtml()
        mh.saveHtml(path, str(num))

        g.get_screen(abspath('dataGenerator/data/html'), str(num))


if __name__=='__main__':
    make_dir()
    make_data(100)