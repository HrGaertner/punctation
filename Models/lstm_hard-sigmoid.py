import numpy as np
import tensorflow.keras.callbacks
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding
from tensorflow.keras.models import Model
import pickle

early = tensorflow.keras.callbacks.EarlyStopping(monitor='loss',
                                                 min_delta=0.03,
                                                 patience=2,
                                                 verbose=0, mode='auto')

(train_data, train_targets), (test_data, test_targets) = pickle.load(open("dataset.pickle", "rb"))

train_data, train_targets = np.array(train_data), np.array(train_targets)


def create_lstm_model(vocab_size, embedding_size=None, embedding_weights=None):
    message = Input(shape=40, dtype='int32', name='lstm_input')
    embedding = Embedding(mask_zero=False, input_dim=55,
                          output_dim=128,
                          trainable=True,
                          name='lstm_embedding')(message)

    lstm_1 = LSTM(units=128, return_sequences=False)(embedding)
    preds = Dense(40, activation='hard_sigmoid', name='lstm_predictions')(lstm_1)

    model = Model(
        inputs=[message],
        outputs=[preds],
    )
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model


lstm_model = create_lstm_model(40, )
lstm_model.save("lstm_sigmoid_punctator")
lstm_model.summary()
lstm_model.fit(train_data, train_targets, epochs=12, batch_size=1024, callbacks=[early])
lstm_model.save_weights("lstm_sigmoid_punctator.h5")
lstm_model.evaluate(test_data, test_targets)