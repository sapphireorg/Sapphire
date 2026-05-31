from importlib.resources import files
import random

class SapphireZero:
    def __init__(self, prompt):
        self.inputs = files("sapphire").joinpath("model/zero/inputs.txt").read_text(encoding="utf-8")
        self.altinputs = files("sapphire").joinpath("model/zero/altinputs.txt").read_text(encoding="utf-8")
        self.outputs = files("sapphire").joinpath("model/zero/outputs.txt").read_text(encoding="utf-8")

        self.response = []
        self.done_outputting = 0
        self.get_sentences(prompt)
        if len(self.sentences) > 2:
            self.set_model("Detailed")
        else:
            self.set_model("Instant")

        sentence_index = 0
        while not sentence_index == len(self.sentences) - 1:
            if not self.sentences[sentence_index] == "":
                self.tokenize(self.sentences[sentence_index])
                self.get_numbers(self.sentences[sentence_index])
                self.repeat_and_get_total()
                self.create_content()
            sentence_index += 1
        self.done_outputting = 1

    def output(self):
        return self.response

    def get_sentences(self, prompt):
        self.sentences = [""]
        for i in prompt:
            if i in "!?.":
                self.sentences.append("")
            else:
                self.sentences[-1] += i

    def set_model(self, model):
        if model == "Detailed":
            self.upper_factor = 0.2
            self.model_type = "Detailed"
        elif model == "Instant":
            self.upper_factor = 0.6
            self.model_type = "Instant"

    def tokenize(self, sentence):
        self.tokens = [""]
        index = 0
        for i in sentence:
            if i == " " and sentence[index + 1] != " ":
                self.tokens.append("")
            elif not i in "?!._[]()/\\|," and i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-+/*":
                self.tokens[-1] += i
            index += 1

    def get_numbers(self, sentence):
        self.numbers = [""]
        index = 0
        for i in sentence:
            if not i in "1234567890" and not self.numbers[-1] == "":
                self.numbers.append(i)
            elif i in "1234567890":
                self.numbers[-1] += i
            elif i == "-" and (sentence[index - 1] in "1234567890" or sentence[index - 2] in "1234567890"):
                self.numbers[-1] += i
            index += 1


    def repeat_and_get_total(self):
        pass

    def create_content(self):
        pass
    