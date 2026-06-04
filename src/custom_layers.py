import tensorflow as tf
layers = tf.keras.layers

class SkillAttentionLayer(layers.Layer):
  """
  Custom Layer: attention mechanism untuk fitur TF-IDF.
  Belajar memberi bobot pada fitur yang relevan untuk match prediction.
  """
  def __init__(self, units: int = 64, **kwargs):
    super().__init__(**kwargs)
    self.units       = units
    self.attention   = layers.Dense(units, activation="tanh")
    self.project_out = layers.Dense(units, activation="linear")

  def call(self, inputs):
    attn = tf.nn.softmax(self.attention(inputs), axis=-1)
    return self.project_out(inputs) * attn

  def get_config(self):
    config = super().get_config()
    config.update({"units": self.units})
    return config

print("SkillAttentionLayer defined.")