import tensorflow as tf
from tensorflow import keras

def urgency_model(max_vocabulary):
    model = keras.Sequential([
        keras.layers.Embedding(max_vocabulary, 32, input_length=500),
        keras.layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'),
        keras.layers.MaxPooling1D(pool_size=2),
        keras.layers.Flatten(),
        keras.layers.Dense(250, activation='relu'),
        keras.layers.Dropout(.025),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model
