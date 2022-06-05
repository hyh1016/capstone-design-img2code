from __future__ import absolute_import

from keras.layers import Input, Dense, Dropout, \
                         RepeatVector, LSTM, concatenate, \
                         Conv2D, MaxPooling2D, Flatten
from keras.models import Sequential, Model
from keras.optimizer_v2.rmsprop import RMSprop
from keras import *
from .Config import *
from .AModel import *


class SplittedPix2codeVisual:
    def __init__(self, model: Model):
        # image모델 split
        visual_input = model.get_layer('input_1').output
        cnn = model.get_layer('sequential')(visual_input)
        self.model = Model(visual_input, cnn)
        
    def predict(self, image):
        return self.model.predict([image], verbose=0)[0]
    
    def predict_batch(self, images):
        return self.model.predict(images, verbose=1)