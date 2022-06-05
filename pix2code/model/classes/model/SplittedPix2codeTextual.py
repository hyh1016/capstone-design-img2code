from __future__ import absolute_import

from keras.layers import Input, Dense, Dropout, \
                         RepeatVector, LSTM, concatenate, \
                         Conv2D, MaxPooling2D, Flatten
from keras.models import Sequential, Model
from keras.optimizer_v2.rmsprop import RMSprop
from keras import *
from .Config import *
from .AModel import *


class SplittedPix2codeTextual:
    def __init__(self, model: Model):
        # 나머지 textual model
        encoded_image_input = Input(shape=(48,1024))
        textual_input = model.get_layer('input_2')
        encoded_text = model.get_layer('sequential_1')(textual_input.output)
        decoder = concatenate([encoded_image_input, encoded_text])
        decoder = model.get_layer('lstm_2')(decoder)
        decoder = model.get_layer('lstm_3')(decoder)
        decoder = model.get_layer('dense_2')(decoder)
        self.model = Model(inputs=[encoded_image_input, textual_input.output], outputs=decoder)
    
    def predict(self, encoded_image, partial_caption):
        return self.model.predict([encoded_image, partial_caption], verbose=0)[0]
    def predict_batch(self, encoded_images, partial_captions):
        return self.model.predict([encoded_images, partial_captions], verbose=1)