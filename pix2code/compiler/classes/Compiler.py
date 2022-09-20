#!/usr/bin/env python
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import json
from .Node import *


class Compiler:
    def __init__(self, dsl_mapping):
        # with open(dsl_mapping_file_path) as data_file:
            # self.dsl_mapping = json.load(data_file)
        self.dsl_mapping = dsl_mapping

        self.opening_tag = self.dsl_mapping["opening-tag"]
        self.closing_tag = self.dsl_mapping["closing-tag"]
        self.content_holder = self.opening_tag + self.closing_tag

        self.root = Node("body", None, self.content_holder)

    def compile(self, input_file_path='', output_file_path='', input_str='', rendering_function=None):
        if input_file_path!='':
            dsl_file = open(input_file_path)
        else:
            dsl_file = input_str.split('\n')

        current_parent = self.root

        for token in dsl_file:
            token = token.replace(" ", "").replace("\n", "")
            if token=='':
                continue
            
            if token.find(self.opening_tag) != -1:
                token = token.replace(self.opening_tag, "")

                element = Node(token, current_parent, self.content_holder)
                current_parent.add_child(element)
                current_parent = element
            elif token.find(self.closing_tag) != -1:
                current_parent = current_parent.parent
            else:
                tokens = token.split(",")
                for t in tokens:
                    element = Node(t, current_parent, self.content_holder)
                    current_parent.add_child(element)

        output_html = self.root.render(self.dsl_mapping, rendering_function=rendering_function)
        if output_file_path!='':
            with open(output_file_path, 'w') as output_file:
                output_file.write(output_html)
        else:
            return output_html
