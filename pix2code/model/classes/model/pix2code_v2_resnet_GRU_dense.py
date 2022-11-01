from __future__ import absolute_import

from sklearn import metrics
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import tensorflow as tf
from keras.layers import Input, Dense, Dropout, \
                         RepeatVector, LSTM, concatenate, \
                         Conv2D, MaxPooling2D, Flatten, GRU,  Bidirectional,  BatchNormalization, Activation, AveragePooling2D, Add, GlobalAveragePooling2D
from keras.models import Sequential, Model
from keras.optimizer_v2.rmsprop import RMSprop
from keras import *
from .Config import *
from .AModel import *
from keras.engine.base_layer import Layer
from keras.utils.generic_utils import custom_object_scope

class ResidualBlock(Layer):
    def __init__(self, channels_in, stride=1, **kwargs):
        super(ResidualBlock, self).__init__(**kwargs)
        self.channels_in = channels_in
        self.stride = stride
        self.conv1 = Conv2D(self.channels_in, (1,1), padding='same')
        self.conv2 = Conv2D(self.channels_in, (3,3), padding='same', strides=self.stride)
        self.conv3 = Conv2D(self.channels_in*4, (1,1), padding='same')

        self.bn1 = BatchNormalization()
        self.bn2 = BatchNormalization()
        self.bn3 = BatchNormalization()

        self.downsample = Sequential()
        self.downsample.add(Conv2D(self.channels_in*4, (1,1), strides=self.stride))
        self.downsample.add(BatchNormalization())

    def get_config(self):
        config = super().get_config()
        config.update({
            "channels_in": self.channels_in,
            "stride": self.stride,
        })
        return config

    
    def call(self, inputs, training=None, **kwargs):
        residual = self.downsample(inputs)

        x = self.conv1(inputs)
        # x = self.bn1(x, training=training)
        x = tf.nn.relu(x)
        x = self.conv2(x)
        # x = self.bn2(x, training=training)
        x = tf.nn.relu(x)
        x = self.conv3(x)
        # x = self.bn3(x, training=training)

        output = tf.nn.relu(tf.keras.layers.add([residual, x]))

        return output

class Basicblock(Layer):
    def __init__(self, channels_in, channels_out, use_batch_norm, stride=1, **kwargs):
        super(Basicblock, self).__init__(**kwargs)
        self.channels_in = channels_in
        self.channels_out = channels_out
        self.stride = stride
        self.use_batch_norm = use_batch_norm

        self.conv1 = Conv2D(channels_out, (3,3), padding='same', strides=self.stride)
        self.conv2 = Conv2D(channels_out, (3,3), padding='same', strides=1)

        self.bn1 = BatchNormalization()
        self.bn2 = BatchNormalization()


        if channels_in == channels_out:
            self.downsample = None
        else:
            self.downsample = Conv2D(channels_out, (1,1), strides=self.stride, padding='same')

    def get_config(self):
        config = super().get_config()
        config.update({
            "channels_in": self.channels_in,
            "channels_out": self.channels_out,
            "use_batch_norm": self.use_batch_norm,
            "stride": self.stride,
        })
        return config
    
    def call(self, inputs, **kwargs):
        identity = inputs

        x = self.conv1(inputs)
        if self.use_batch_norm:
            x = self.bn1(x)
        x = tf.nn.relu(x)
        x = self.conv2(x)
        if self.use_batch_norm:
            x = self.bn2(x)

        if self.downsample is not None:
                identity = self.downsample(inputs)

        output = tf.nn.relu(tf.keras.layers.add([x, identity]))
        return output

class pix2code_v2_resnet_GRU_dense(AModel):
    def __init__(self, input_shape, output_size, output_path):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "pix2code_v2_resnet_GRU_dense"

        #CNN Layer: 입력된 이미지에서 feature 추출
        image_model = Sequential()
        image_model.add(Conv2D(32, (7, 7), padding='same' ,input_shape=input_shape, strides=1))
        # image_model.add(BatchNormalization())
        image_model.add(Activation('relu'))
        image_model.add(MaxPooling2D(pool_size=(3, 3), strides=2, padding='same'))

        image_model.add(Basicblock(32,32,use_batch_norm=False ))
        image_model.add(Basicblock(32,64,use_batch_norm=False, stride=2))
        image_model.add(Basicblock(64,128,use_batch_norm=False, stride=2))
        image_model.add(Basicblock(128,256,use_batch_norm=False, stride=2))

        image_model.add(AveragePooling2D(2,2))
        image_model.add(Flatten())
        image_model.summary()

        #LSTM encoder: dsl언어를 학습하는 언어모델
        language_model = Sequential()
        language_model.add(GRU(1024, return_sequences=True, input_shape=(CONTEXT_LENGTH, output_size)))
        language_model.add(GRU(1024, return_sequences=True))

        #image Encoder: 이미지의 feature와 언어모델의 결과를 받아 보다 정교한 이미지 feature 추출(이미지에 현재 진행 상태 정보를 알려줌)
        image_post_model = Sequential()
        image_post_model.add(Dense(1024, activation='relu'))
        image_post_model.add(Dropout(0.3))
        image_post_model.add(Dense(1024, activation='relu'))
        image_post_model.add(Dropout(0.3))
        image_post_model.add(RepeatVector(CONTEXT_LENGTH))

        textual_input = Input(shape=(CONTEXT_LENGTH, output_size))
        encoded_text = language_model(textual_input)
        flatten_encoded_text = Flatten()(encoded_text)

        #decoder로 들어가는 언어 모델 결과 확장
        encoded_text = Dense(1024, activation='relu')(encoded_text)

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