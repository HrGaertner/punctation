import numpy as np
import keras.callbacks
from keras.layers import Input, Dense, LSTM, Embedding, Activation
from keras.models import Model
import keras.backend as tf
from keras.utils.generic_utils import get_custom_objects
import pickle

early = keras.callbacks.EarlyStopping(monitor='loss',
                                                 min_delta=0.03,
                                                 patience=2,
                                                 verbose=0, mode='auto')

with open("dataset.pickle", "rb") as f:
    (features, vectors) = pickle.load(f)

train_data = features[:int(len(features)*0.9)] #Splitting data into teining and test dataset
test_data = features[int(len(features)*0.9)]
train_targets = vectors[:int(len(vectors)*0.9)]
test_targets = vectors[int(len(vectors)*0.9):]

with open("dataset.pickle", "wb") as f:
    pickle.dump(((train_data, train_targets), (test_data, test_targets)), f)

#(train_data, train_targets), (test_data, test_targets) = pickle.load(open("dataset_bad.pickle", "rb"))

train_data, train_targets = np.array(train_data), np.array(train_targets)

def unit_step_activation(x):
    return tf.sign(x)

get_custom_objects().update({'unit_step_activation': Activation(unit_step_activation)})

def create_lstm_model(vocab_size, embedding_size=None, embedding_weights=None):
    message = Input(shape=(20,), dtype='int32', name='lstm_input')
    embedding = Embedding(mask_zero=False, input_dim=55,
                          output_dim=128,
                          trainable=True,
                          name='lstm_embedding')(message)

    lstm_1 = LSTM(units=128, return_sequences=False)(embedding)
    preds = Dense(20, activation='hard_sigmoid', name='lstm_predictions')(lstm_1)
    unit_step = Dense(20, activation=unit_step_activation, name="clear_ouput")(preds)

    model = Model(
        inputs=[message],
        outputs=[unit_step],
    )
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model


lstm_model = create_lstm_model(40, )
lstm_model.save("unit_step-punctator")
lstm_model.summary()
lstm_model.fit(train_data, train_targets, epochs=1, batch_size=1024, callbacks=[early])
lstm_model.save_weights("unit_step-punctator.h5")
lstm_model.evaluate(test_data, test_targets)