from sklearn.externals import joblib
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "infersent"))



def load_model(model='data/model.pkl', glove_path='data/glove.840B.300d.txt', infersent_path='data/infersent.allnli.pickle'):
    """
    :param model:  path to the model which should be loaded
    :param glove_path:  path to the glove embeddings
    :param infersent_path: path to the saved infersent model
    :return:
    """
    model = joblib.load(model)
    if glove_path and infersent_path:
        model.named_steps['infersentfeature'].glove_path = glove_path
        model.named_steps['infersentfeature'].infersent_path = infersent_path

    return model

