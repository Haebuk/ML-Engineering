import tensorflow as tf
import wandb 
from wandb.keras import WandbCallback

default_config = {
    'learning_rate': 0.02,
    'dropout_rate': 0.3,
    'hidden1': 256,
    'activation1': 'tanh'
}
wandb.init(project='mnist-tf2-sweep', config=default_config)
config = wandb.config
#config.learning_rate = 0.02
#config.dropout_rate = 0.3
#config.hidden1 = 256
#config.activation1 = 'tanh'

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0,  x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(config.hidden1, activation=config.activation1),
    tf.keras.layers.Dropout(config.dropout_rate),
    tf.keras.layers.Dense(10, activation='softmax')
])
opt = tf.keras.optimizers.Adam(learning_rate=config.learning_rate)
model.compile(optimizer=opt,
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])

model.fit(x_train, y_train, 
          validation_data = (x_test, y_test), # 중간중간에 성능 체크
          epochs=5, callbacks=[WandbCallback()])

model.evaluate(x_test, y_test, verbose=2)