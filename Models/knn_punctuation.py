from tensorflow.keras import models
from tensorflow.keras import layers
import numpy as np
import pickle

with open("feature.pickle", "rb") as f: #Loading prepocessed data
    features = np.array(pickle.load(f))

with open("vec.pickle", "rb") as f:
    vectors = np.array(pickle.load(f))

#train_data = features[:int(len(features)*0.9)] #Splitting data into teining and test dataset
#test_data = features[int(len(features)*0.9)]
#train_targets = vectors[:int(len(vectors)*0.9)]
#test_targets = vectors[int(len(vectors)*0.9):]

model = models.Sequential()
model.add(layers.Dense(32, activation="relu", input_shape=(40,)))
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(40, activation="softmax"))
model.compile(optimizer="rmsprop", loss="mse")
model.summary()
model.fit(features, vectors, epochs=500, batch_size=20, verbose=0)
model.save("punctator")
model.save_weights("punctator.h5")

print(model.evaluate(test_data, test_targets))
