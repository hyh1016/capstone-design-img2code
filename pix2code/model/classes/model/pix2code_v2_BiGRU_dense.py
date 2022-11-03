from __future__ import absolute_import

from sklearn import metrics
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

from keras.layers import Input, Dense, Dropout, \
                         RepeatVector, LSTM, concatenate, \
                         Conv2D, MaxPooling2D, Flatten, GRU, Bidirectional
from keras.models import Sequential, Model
from keras.optimizer_v2.rmsprop import RMSprop
from keras import *
from .Config import *
from .AModel import *


class pix2code_v2_BiGRU_dense(AModel):
    def __init__(self, input_shape, output_size, output_path):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "pix2code_v2_BiGRU_dense"

        #CNN Layer: 입력된 이미지에서 feature 추출
        image_model = Sequential()
        image_model.add(Conv2D(32, (3, 3), padding='valid', activation='relu', input_shape=input_shape))
        image_model.add(Conv2D(32, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))

        image_model.add(Conv2D(64, (3, 3), padding='valid', activation='relu'))
        image_model.add(Conv2D(64, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))

        image_model.add(Conv2D(128, (3, 3), padding='valid', activation='relu'))
        image_model.add(Conv2D(128, (3, 3), padding='valid', activation='relu'))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Flatten())

        #LSTM encoder: dsl언어를 학습하는 언어모델
        language_model = Sequential()
        language_model.add(Bidirectional(GRU(512, return_sequences=True, input_shape=(CONTEXT_LENGTH, output_size))))
        language_model.add(Bidirectional(GRU(512, return_sequences=True)))

        #image Encoder: 이미지의 feature와 언어모델의 결과를 받아 보다 정교한 이미지 feature 추출(이미지에 현재 진행 상태 정보를 알려줌)
        image_post_model = Sequential()
        image_post_model.add(Dense(1024, activation='relu'))
        image_post_model.add(Dropout(0.2))
        image_post_model.add(Dense(1024, activation='relu'))
        image_post_model.add(Dropout(0.2))
        image_post_model.add(RepeatVector(CONTEXT_LENGTH))

        textual_input = Input(shape=(CONTEXT_LENGTH, output_size))
        encoded_text = language_model(textual_input)
        flatten_encoded_text = Flatten()(encoded_text)

        #decoder로 들어가는 언어 모델 값 처리
        encoded_text = Dense(1024, activation='relu')(encoded_text)
        encoded_text = Dropout(0.2)(encoded_text)

        visual_input = Input(shape=input_shape)
        primary_endcoded_image = image_model(visual_input)

        encoded_features = concatenate([primary_endcoded_image, flatten_encoded_text])
        secondary_endcoded_image = image_post_model(encoded_features)
        
        decoder = concatenate([secondary_endcoded_image, encoded_text])

        #decoder: 이미지와 언어모델의 feature를 받아 최종 dsl 토큰 결정
        decoder = GRU(1024, return_sequences=True)(decoder)
        decoder = GRU(1024, return_sequences=False)(decoder)
        decoder = Dense(output_size, activation='softmax')(decoder)

        self.model = Model(inputs=[visual_input, textual_input], outputs=decoder)

        optimizer = RMSprop(lr=0.00005, clipvalue=1.0)
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
        return self.model.predict([images, partial_captions], verbose=1)