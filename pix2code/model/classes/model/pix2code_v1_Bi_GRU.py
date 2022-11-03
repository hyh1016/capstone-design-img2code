from __future__ import absolute_import

from sklearn import metrics
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

from keras.layers import Input, Dense, Dropout, \
                         RepeatVector, LSTM, concatenate, \
                         Conv2D, MaxPooling2D, Flatten, GRU
from keras.models import Sequential, Model
from keras.optimizer_v2.rmsprop import RMSprop
from keras.layers import Bidirectional
from keras import *
from .Config import *
from .AModel import *


class pix2code_v1_Bi_GRU(AModel):
    def __init__(self, input_shape, output_size, output_path):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "pix2code_v1_Bi_GRU"

        image_model = Sequential()
        image_model.add(Conv2D(32, (3, 3), padding='valid', activation='relu', input_shape=input_shape))
        image_model.add(Conv2D(32, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.1))

        image_model.add(Conv2D(64, (3, 3), padding='valid', activation='relu'))
        image_model.add(Conv2D(64, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.1))

        image_model.add(Conv2D(128, (3, 3), padding='valid', activation='relu'))
        image_model.add(Conv2D(128, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.1))

        image_model.add(Flatten())
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.1))
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.1))

        image_model.add(RepeatVector(CONTEXT_LENGTH))
        image_model.summary()

        visual_input = Input(shape=input_shape)
        encoded_image = image_model(visual_input)

        language_model = Sequential()
        language_model.add(Bidirectional(GRU(512, return_sequences=True, input_shape=(CONTEXT_LENGTH, output_size))))
        language_model.add(Bidirectional(GRU(512, return_sequences=True)))

        textual_input = Input(shape=(CONTEXT_LENGTH, output_size))
        encoded_text = language_model(textual_input)

        decoder = concatenate([encoded_image, encoded_text])

        decoder = GRU(1024, return_sequences=True)(decoder)
        decoder = GRU(1024, return_sequences=False)(decoder)
        decoder = Dense(output_size, activation='softmax')(decoder)

        self.model = Model(inputs=[visual_input, textual_input], outputs=decoder)

        optimizer = RMSprop(lr=0.000025, clipvalue=1.0,  rho=0.8)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model.summary()

    def fit(self, images, partial_captions, next_words, callbacks):
        self.model.fit([images, partial_captions], next_words, shuffle=False, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, callbacks=callbacks)
        self.save()

    def fit_generator(self, generator, valid_generator, steps_per_epoch, validation_steps, callbacks):
        self.model.fit_generator(generator, steps_per_epoch=steps_per_epoch, epochs=EPOCHS, verbose=1, callbacks=callbacks, validation_data=valid_generator, validation_steps=validation_steps)
        self.save()

    def predict(self, image, partial_caption):
        return self.model.predict([image, partial_caption], verbose=0)[0]

    def predict_batch(self, images, partial_captions):
        return self.model.predict([images, partial_captions], verbose=0)