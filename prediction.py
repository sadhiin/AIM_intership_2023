import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class PredictionPipeline:
    def __init__(self, model: tf.keras.models) -> None:
        self.model = tf.keras.models.load_model(model)
        self.max_features = 1500

        tokenizer = Tokenizer(num_words= self.max_features, split=' ')

    def predict(self, text: str) -> str:
        cmnt = self.tokenizer.texts_to_sequences([text])
        cmnt = pad_sequences(cmnt, maxlen=203)

        return np.argmax(self.model.predict(cmnt)[0])