from HtmlToPng import *
from MakeHtml import MakeHtml
import RandomDSL
from RandomDSL import *
from posixpath import abspath
import os
import uuid
import argparse

path = 'dataGenerator/data/'
def make_dir():
    os.makedirs('./dataGenerator/data/dsl', exist_ok=True)
    os.makedirs('./dataGenerator/data/html', exist_ok=True)
    os.makedirs('./dataGenerator/data/png', exist_ok=True)

def make_data(iter: int):
    rd = Dsl()
    g = HtmlToPng()
    for num in range(iter):
        fileName = str(uuid.uuid4()).upper()
        with open(path+'dsl/'+fileName+'.gui', 'w') as f:
            f.write(rd.getDsl()[1:])
        
        mh = MakeHtml()
        mh.saveHtml(path, fileName)

        g.get_screen(abspath('dataGenerator/data/html'), fileName)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='make data')
    parser.add_argument('cnt', type=int)
    args = parser.parse_args()
    
    make_dir()
    make_data(args.cnt)