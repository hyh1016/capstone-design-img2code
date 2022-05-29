


import string
import random
from compiler.classes.Compiler import *
from compiler.classes.Utils import *

TEXT_PLACE_HOLDER = "[]"
def render_content_with_text(key, value):
    if key.find("btn") != -1:
        value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text())
    elif key.find("title") != -1:
        value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
    elif key.find("text") != -1:
        value = value.replace(TEXT_PLACE_HOLDER,
                                Utils.get_random_text(length_text=56, space_number=7, with_upper_case=False))
    return value

class MakeHtml:

    def __init__(self) -> None:
        dsl_path = 'pix2code/compiler/assets/web-dsl-mapping.json'
        self.compiler = Compiler(dsl_path)

    def saveHtml(self, path: string, filename: string) -> None:
        dsl = '{}/dsl/{}.gui'.format(path, filename)
        html = '{}/html/{}.html'.format(path, filename)
        self.compiler.compile(dsl, html, rendering_function=render_content_with_text)


if __name__=='__main__':
    mh = MakeHtml()
    mh.saveHtml('dataGenerator/data', '1')