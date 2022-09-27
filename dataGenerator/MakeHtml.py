


import string
import random
from pix2code.compiler.classes.DSLMapper import DSLMapper
from pix2code.compiler.classes.Compiler import *
from pix2code.compiler.classes.Utils import *
from pix2code.compiler.web_compiler import render_content_with_example_text, render_content_with_random_text

class MakeHtml:

    def __init__(self) -> None:
        dsl_path = 'pix2code/compiler/assets/class-group.json'
        dsl_mapper = DSLMapper(dsl_path)
        dsl_mapping = dsl_mapper.get_dsl_mapping()

        self.compiler = Compiler(dsl_mapping)

    def saveHtml(self, path: string, filename: string) -> None:
        dsl = '{}/dsl/{}.gui'.format(path, filename)
        html = '{}/html/{}.html'.format(path, filename)
        self.compiler.compile(dsl, html, rendering_function=render_content_with_random_text)


if __name__=='__main__':
    mh = MakeHtml()
    mh.saveHtml('dataGenerator/data', '1')