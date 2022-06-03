#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
from gc import callbacks
from tensorflow import keras
import sys

from classes.dataset.Generator import *
from classes.model.pix2code import *

import os
import tensorflow as tf
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))


def run(input_path, output_path, pretrained_model=None):
    np.random.seed(1234)

    dataset = Dataset()
    dataset.load(input_path, generate_binary_sequences=True)
    dataset.save_metadata(output_path)
    dataset.voc.save(output_path)

    gui_paths, img_paths = Dataset.load_paths_only(input_path)
    input_shape = dataset.input_shape
    output_size = dataset.output_size
    steps_per_epoch = dataset.size / BATCH_SIZE

    voc = Vocabulary()
    voc.retrieve(output_path)

    generator = Generator.data_generator(voc, gui_paths, img_paths, batch_size=BATCH_SIZE, generate_binary_sequences=True)

    model = pix2code(input_shape, output_size, output_path)

    model.model.load_weights(pretrained_model)

if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 2:
        print("Error: not enough argument supplied:")
        print("train.py <input path> <output path> <is memory intensive (default: 0)> <pretrained weights (optional)>")
        exit(0)
    else:
        input_path = argv[0]
        output_path = argv[1]
        use_generator = False if len(argv) < 3 else True if int(argv[2]) == 1 else False
        pretrained_weigths = None if len(argv) < 4 else argv[3]

    run(input_path, output_path, pretrained_model=pretrained_weigths)