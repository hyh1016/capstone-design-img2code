import sys

from os.path import basename
from pix2code.model.classes.Sampler import *
from pix2code.model.classes.model.pix2code import *
from pix2code.model.classes.model.pix2code_v1 import *
from pix2code.model.classes.model.pix2code_v1_Bi_GRU import *
from pix2code.model.classes.model.pix2code_v2_GRU_dense import *

PROCESS_COUNT = 32

def predict_greedy_multi(input_img, inQueue:Queue, outQueue:Queue, id, voc:Vocabulary, input_shape, output_size, context_length, require_sparse_label=True, sequence_length=150, verbose=False):
    current_context = [voc.vocabulary[PLACEHOLDER]] * (context_length - 1)
    current_context.append(voc.vocabulary[START_TOKEN])
    if require_sparse_label:
        current_context = Utils.sparsify(current_context, output_size)

    predictions = START_TOKEN
    out_probas = []

    for i in range(0, sequence_length):
        if verbose:
            print("predicting {}/{}...".format(i, sequence_length))

        # 멀티 프로세싱 처리
        ##################
        inQueue.put((input_img, np.array([current_context]), id))
        probas = outQueue.get()
        # while True:
        #     if not outQueue.empty():
        #         probas = outQueue.get()
        #         break
        ##################

        # probas = model.predict(input_img, np.array([current_context]))
        prediction = np.argmax(probas)
        out_probas.append(probas)

        new_context = []
        for j in range(1, context_length):
            new_context.append(current_context[j])

        if require_sparse_label:
            sparse_label = np.zeros(output_size)
            sparse_label[prediction] = 1
            new_context.append(sparse_label)
        else:
            new_context.append(prediction)

        current_context = new_context

        predictions += voc.token_lookup[prediction]

        if voc.token_lookup[prediction] == END_TOKEN:
            break

    return predictions, out_probas

from multiprocessing import Queue, Process, Pool
import multiprocessing as mp
import os
from tqdm import tqdm

# queue 입력 데이터
# [input_img, current_context, qid]
def doPredict(model:pix2code_v1_Bi_GRU, input_imgs, current_contexts, ids, outQueue:list):
    result = model.predict_batch(input_imgs, current_contexts)
    for i, id in enumerate(ids):
        outQueue[id].put(result[i])

def predictDsl(input_path, output_path, trained_weights_path, inQueue:Queue, outQueue:Queue, input_shape, output_size, qnum:int):
    voc = Vocabulary()
    voc.retrieve(trained_weights_path)
    
    file_list = os.listdir(input_path)
    file_list1 = set(os.listdir(output_path))
    file_list = file_list[qnum::PROCESS_COUNT]
    for input_file in file_list:
        if basename(input_file)[:basename(input_file).find(".")]+'.gui' in file_list1:
            print("skip {}".format(input_file))
            continue
        file_name = basename(input_file)[:basename(input_file).find(".")]
        evaluation_img = Utils.get_preprocessed_img(input_path + input_file, IMAGE_SIZE)
        result, _ = predict_greedy_multi(np.array([evaluation_img]), inQueue, outQueue, qnum, voc, input_shape, output_size, CONTEXT_LENGTH)
        result = result.replace('<START>', '').replace('<END>', '').replace('{', ' {').replace(',', ', ')
        with open(f'{output_path}{file_name}.gui', 'w') as f:
            f.write(result)
        # print('Predicted DSL for {}.'.format(input_file))
        # print(result)
        # print('-----------------------')


def worker(trained_weights_path:str, inQueue:mp.Queue, outQueue:mp.Queue):
    meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path), allow_pickle=True)
    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    model = pix2code_v2_GRU_dense(input_shape, output_size, trained_weights_path)
    model.load('pix2code_v2_GRU_dense')
    
    input_imgs = np.empty((0, 256, 256, 3))
    current_contexts = np.empty((0, 48, 23))
    ids = []
    cnt = 0
    while True:
        if inQueue.empty():
            if cnt==0:
                continue
            doPredict(model, input_imgs, current_contexts, ids, outQueue)
            input_imgs = np.empty((0, 256, 256, 3))
            current_contexts = np.empty((0, 48, 23))
            ids = []
            cnt = 0
            continue
        data = inQueue.get()
        if data==None:
            break
        input_imgs = np.append(input_imgs, data[0], axis=0)
        current_contexts = np.append(current_contexts, data[1], axis=0)
        ids.append(data[2])
        cnt += 1
        # PROCESS_COUNT개 찼을 때 처리
        if cnt == PROCESS_COUNT//2:
            doPredict(model, input_imgs, current_contexts, ids, outQueue)
            input_imgs = np.empty((0, 256, 256, 3))
            current_contexts = np.empty((0, 48, 23))
            ids = []
            cnt = 0

def main_process(inQueue:mp.Queue, outQueue:list, trained_weights_path:str, data_path:str):
    meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path), allow_pickle=True)
    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]
    input_path = f'{data_path}/png/'
    output_path = f'{data_path}/dsl_predict/'

    procs = []
    for i in range(PROCESS_COUNT):
        # predictDsl(input_path, output_path, file_lists[i], inQueue, outQueue[i], input_shape, output_size, i)
        # print(input_path, output_path, inQueue, outQueue[i], input_shape, output_size, i)
        p = Process(target=predictDsl, args=(input_path, output_path, trained_weights_path, inQueue, outQueue[i], input_shape, output_size, i, ))
        p.start()
        procs.append(p)
    
    import time
    time.sleep(1)
    workerProc = Process(target=worker, args=(trained_weights_path, inQueue, outQueue))
    workerProc.start()

    for p in procs:
        p.join()
    inQueue.put(None)
    workerProc.join()

if __name__ == '__main__':
    trained_weights_path='pix2code/bin/tag_extension/v2_GRU_dense'
    data_path = 'dataGenerator/data/7'
    inQueue = mp.Queue()
    outQueue = [mp.Queue() for _ in range(PROCESS_COUNT)]
    main_process(inQueue, outQueue, trained_weights_path, data_path)
