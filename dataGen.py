from dataGenerator.HtmlToPng import *
from dataGenerator.MakeHtml import MakeHtml
import dataGenerator.RandomDSL
from dataGenerator.RandomDSL import *
from posixpath import abspath
import os
import uuid
import argparse
from tqdm import tqdm
import multiprocessing as mult

path = 'dataGenerator/data/'
def make_dir():
    os.makedirs('./dataGenerator/data/dsl', exist_ok=True)
    os.makedirs('./dataGenerator/data/html', exist_ok=True)
    os.makedirs('./dataGenerator/data/png', exist_ok=True)

def make_data(iter: int):
    rd = Dsl()
    g = HtmlToPng()
    for num in tqdm(range(iter)):
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
    
    procs = []
    make_dir()
    for i in range(25):
        p = mult.Process(target=make_data, args=(args.cnt,))
        p.start()
        procs.append(p)
    
    for p in procs:
        p.join()