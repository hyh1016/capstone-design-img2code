import sys
from os.path import basename
from flask import Flask, jsonify, request
from pix2code.model.classes.Sampler import *
from pix2code.model.classes.model.pix2code import *
from pix2code.model.classes.Utils import *
from pix2code.compiler.classes.Compiler import *
from pix2code.compiler.classes.DSLMapper import *
from pix2code.compiler.web_compiler import render_content_with_example_text, render_content_with_random_text

app = Flask(__name__)

# 모델 경로 지정
trained_weights_path='pix2code/bin'
trained_model_name='pix2code_v1'

# 모델 로드
meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path), allow_pickle=True)
input_shape = meta_dataset[0]
output_size = meta_dataset[1]
model = pix2code(input_shape, output_size, trained_weights_path)
model.load(trained_model_name)

sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

# 컴파일러 로드
dsl_mapper = DSLMapper("pix2code/compiler/assets/class-group.json")
dsl_mapping = dsl_mapper.get_dsl_mapping()
compiler = Compiler(dsl_mapping)


@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']
    # 예측
    evaluation_img = Utils.get_preprocessed_img_bytes(image.read(), IMAGE_SIZE)
    result, _ = sampler.predict_greedy_(model, np.array([evaluation_img]))
    result = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
    print("Result greedy: {}".format(result))
    # dsl 변환
    html = compiler.compile(input_str=result, rendering_function=render_content_with_example_text)
    print("Result compile: {}".format(html))
    # 리스폰스 객체 생성
    response = jsonify({'html':html})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response