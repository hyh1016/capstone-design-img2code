#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
from gc import callbacks
from tensorflow import keras

__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import tensorflow as tf
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

import sys

from classes.dataset.Generator import *
from classes.model.pix2code import *

import os
dir_name = "Learning_log"

def make_tensorboard_dir(dir_name):
    root_logdir = os.path.join(os.curdir,dir_name)
    sub_dir_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(root_logdir,sub_dir_name)

TB_log_dir = make_tensorboard_dir(dir_name)
TensorB = keras.callbacks.TensorBoard(log_dir = TB_log_dir)

# early_stop = keras.callbacks.EarlyStopping(monitor = "var_loss",min_delta=0, patience=10, restore_best_weights=True)

def run(input_path, output_path, test_path, is_memory_intensive=False, pretrained_model=None):
    np.random.seed(1234)

    dataset = Dataset()
    dataset.load(input_path, generate_binary_sequences=True)
    dataset.save_metadata(output_path)
    dataset.voc.save(output_path)

    vaild_dataset = Dataset()
    vaild_dataset.load(test_path, generate_binary_sequences=True)

    if not is_memory_intensive:
        dataset.convert_arrays()

        input_shape = dataset.input_shape
        output_size = dataset.output_size

        print(len(dataset.input_images), len(dataset.partial_sequences), len(dataset.next_words))
        print(dataset.input_images.shape, dataset.partial_sequences.shape, dataset.next_words.shape)
    else:
        gui_paths, img_paths = Dataset.load_paths_only(input_path)

        input_shape = dataset.input_shape
        output_size = dataset.output_size
        steps_per_epoch = dataset.size / BATCH_SIZE

        voc = Vocabulary()
        voc.retrieve(output_path)

        generator = Generator.data_generator(voc, gui_paths, img_paths, batch_size=BATCH_SIZE, generate_binary_sequences=True)

    model = pix2code(input_shape, output_size, output_path)

    if pretrained_model is not None:
        model.model.load_weights(pretrained_model)

    if not is_memory_intensive:
        model.fit(dataset.input_images, dataset.partial_sequences, dataset.next_words, callbacks=[TensorB])
    else:
        model.fit_generator(generator, vaild_dataset.input_images, vaild_dataset.partial_sequences, vaild_dataset.next_words, steps_per_epoch=steps_per_epoch, callbacks=[TensorB])

if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 2:
        print("Error: not enough argument supplied:")
        print("train.py <input path> <output path> <is memory intensive (default: 0)> <pretrained weights (optional)>")
        exit(0)
    else:
        input_path = argv[0]
        output_path = argv[1]
        test_path = argv[2]
        use_generator = False if len(argv) < 4 else True if int(argv[3]) == 1 else False
        pretrained_weigths = None if len(argv) < 5 else argv[4]

    run(input_path, output_path, test_path, is_memory_intensive=use_generator, pretrained_model=pretrained_weigths)