import torch


class InfersentFeature:

    def __init__(self, model):
        self.model = model

    def __init__(self, glove_path, infersent_path):
        self.model = None
        self.infersent_path = infersent_path
        self.glove_path = glove_path

    def transform(self, sentences):
        infersent = torch.load(self.infersent_path, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(self.glove_path)
        infersent.build_vocab(sentences, tokenize=True)
        encode = infersent.encode(sentences, tokenize=True)
        return encode

    def fit(self, X, y):
        return self
