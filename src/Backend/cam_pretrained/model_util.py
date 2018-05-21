from sklearn.externals import joblib

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
#from xgboost import XGBClassifier

from cam_pretrained.data_extraction import ExtractMiddlePart
from cam_pretrained.infersent.infersent_feature import InfersentFeature

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "infersent"))


def save_model(train_data, glove_path='glove.840B.300d.txt', infersent_path='infersent.allnli.pickle', output_file='data/model.pkl'):
   train = pd.read_csv(train_data, encoding = "utf8")
   pl = make_pipeline(ExtractMiddlePart(), InfersentFeature(glove_path, infersent_path), LogisticRegression()) #XGBClassifier(n_jobs=8, n_estimators=1000))

   fitted = pl.fit(train, train['most_frequent_label'].values)
   joblib.dump(fitted, output_file, compress=0)


def save_bow_model(train_data, output_file='data/model.pkl'):
    """

    :param train_data: training input
    :param output_file: model output
    :return: model trained on a simple bag-of-words feature
    """
    train = pd.read_csv(train_data)
    pl = make_pipeline(ExtractMiddlePart(), CountVectorizer(), LogisticRegression())
    fitted = pl.fit(train, train['most_frequent_label'].values)
    joblib.dump(fitted, output_file, compress=0)


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
