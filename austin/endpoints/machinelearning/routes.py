from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required

import tensorflow as tf
from tensorflow import keras
import os

from .utils import load_md
from .urgency_model import urgency_model
from austin.config import Config

ml = Blueprint('ml', __name__)


@ml.route('/urgency')
def index():
    html = load_md("urgency.md")
    return render_template('machinelearning/urgency.html', md=html)


@ml.route('/classify', methods=['POST'])
def classify():
    model = urgency_model(10000)
    filepath = Config.APP_ROOT + "/models/ml_models/cp.ckpt"
    model.load_weights(filepath)

    text = request.form.get('ticket_body')
    matrix = keras.preprocessing.text.one_hot(text, 10000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')

    matrix = keras.preprocessing.sequence.pad_sequences([matrix], maxlen=500)

    # Prediction
    probability = model.predict(matrix)
    prediction_label = probability.argmax(axis=-1)
    print(prediction_label)

    html = load_md("urgency.md")
    return render_template('machinelearning/urgency_prediction.html', prediction=prediction_label, md=html)
