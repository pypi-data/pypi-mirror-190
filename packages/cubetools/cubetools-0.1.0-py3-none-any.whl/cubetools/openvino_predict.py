# -*- coding:utf-8 -*-
from openvino.runtime import Core


# 基于OpenVino推理引擎封装的通用OpenVino推理器
class OpenvinoPredict(object):
    def __init__(self, model, device='AUTO'):
        self.core = Core()
        self.model = self.core.read_model(model=model)
        self.compiled_model = self.core.compile_model(model=self.model, device_name=device)
        self.input_keys = self.compiled_model.inputs
        self.output_keys = self.compiled_model.outputs

    def predict(self, inputs: list) -> list:
        input_dict = {}
        for input in zip(self.input_keys, inputs):
            input_dict[input[0]] = input[1]

        results = self.compiled_model(input_dict)

        outputs = []
        for output_key in self.output_keys:
            outputs.append(results[output_key])

        return outputs
