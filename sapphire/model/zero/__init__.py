from importlib.resources import files
import random
import math

class SapphireZero:
    def __init__(self, prompt):
        self.inputs = files("sapphire").joinpath("model/zero/inputs.txt").read_text(encoding="utf-8").split("\n")
        self.altinputs = files("sapphire").joinpath("model/zero/altinputs.txt").read_text(encoding="utf-8").split("\n")
        self.outputs = files("sapphire").joinpath("model/zero/outputs.txt").read_text(encoding="utf-8").split("\n")

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
        get_total_index = 0
        self.total_for_each_train = []
        for i in self.inputs:
            tmp_tokens = i.split(" ")
            token_loop = 0
            total_word_count = 0
            for j in tmp_tokens:
                if tmp_tokens[token_loop] in j:
                    total_word_count += 1
                token_loop += 1
            self.total_for_each_train.append(total_word_count)

            tmp_tokens = self.altinputs[get_total_index].split(" ")
            token_loop = 0
            total_word_count = 0
            for j in tmp_tokens:
                if tmp_tokens[token_loop] in j:
                    total_word_count += 1
                token_loop += 1
            if total_word_count > self.total_for_each_train[-1]:
                self.total_for_each_train[-1] = total_word_count
            get_total_index += 1


    def create_content(self):
        content_for_response = ""
        self.outputs_to_use = []
        factor = 1
        while not (factor < self.upper_factor) or not ((len(self.outputs_to_use) > math.ceil(3.77 / self.upper_factor)) or (len(self.outputs_to_use) > 1)):
            if factor < self.upper_factor:
                break

            token_loop = 0
            for i in self.total_for_each_train:
                if (len(self.tokens) * factor <= int(i)):
                    if (not len(self.tokens) > math.ceil(3 / self.upper_factor)) or self.outputs[token_loop] in self.outputs_to_use:
                        self.outputs_to_use.append(self.outputs[token_loop])
                token_loop += 1
            factor -= 0.05
        
        self.response.append(self.outputs_to_use[random.randint(0, len(self.outputs_to_use) - 1)].split(" ")[0])
        for i in range(5, 21):
            self.get_next_word_for_word(self.response[-1])
            if not self.next_word == "":
                self.response.append(self.next_word)
        while not self.response[-1][-1] in "!?." or self.response[-2][-1] in "!?.":
            self.get_next_word_for_word(self.response[-1])
            if not self.next_word == "":
                self.response.append(self.next_word)

    def get_next_word_for_word(self, word):
        total = []
        words = []
        token_loop = 0

        for i in self.outputs_to_use:
            tokens = i.split(" ")
            sub_token_loop = 0
            for j in tokens:
                if j == word:
                    if not ((sub_token_loop + 1 < len(tokens) and self.response[-1] == tokens[sub_token_loop + 1]) or (sub_token_loop - 1 >= 0 and self.response[-1] == tokens[sub_token_loop - 1])):
                        if len(self.response) < 3 or not ((sub_token_loop + 1 < len(tokens) and self.response[-2] == tokens[sub_token_loop + 1]) or (sub_token_loop - 1 >= 0 and self.response[-3] == tokens[sub_token_loop - 1])):
                            if (sub_token_loop + 1) < len(tokens) and tokens[sub_token_loop + 1] != "":
                                words.append(tokens[sub_token_loop + 1])
                                if len(self.response) >= 2 and (sub_token_loop - 1) >= 0 and tokens[sub_token_loop - 1] == self.response[-2]:
                                    total.append(2)
                                else:
                                    total.append(1)
                            elif (sub_token_loop + 1) < len(tokens):
                                total[words.index(tokens[sub_token_loop + 1])] += 1
                sub_token_loop += 1
        
        token_loop = 0
        best_word_total = 0
        self.next_word = ""
        for i in words:
            if token_loop < len(total):
                if (total[token_loop] > best_word_total) or (random.randint(1,3) == 2 and total[token_loop] == best_word_total):
                    best_word_total = total[token_loop]
                    self.next_word = i
            token_loop += 1