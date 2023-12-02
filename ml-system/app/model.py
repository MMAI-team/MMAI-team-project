import tensorflow as tf

AUTOTUNE = tf.data.AUTOTUNE
from tensorflow import keras
from keras import layers
from keras.layers import Dense


class BaseAttention(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__()
        self.mha = tf.keras.layers.MultiHeadAttention(**kwargs)
        self.layernorm = tf.keras.layers.LayerNormalization()
        self.add = tf.keras.layers.Add()


class CausalSelfAttention(BaseAttention):
    def call(self, q, v):
        attn_output = self.mha(query=q, value=v, key=v, use_causal_mask=True)
        x = self.add([v, attn_output])
        x = self.layernorm(x)
        return x


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = CausalSelfAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [
                layers.Dense(ff_dim, activation="relu"),
                layers.Dense(embed_dim),
                layers.Dropout(rate),
            ]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)  # self-attention layer
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)  # layer norm
        ffn_output = self.ffn(out1)  # feed-forward layer
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)  # layer norm


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, len=32, dim=64, **kwargs):
        super(TokenAndPositionEmbedding, self).__init__(**kwargs)
        self.pos_emb = layers.Embedding(input_dim=len, output_dim=dim)
        self.maxlen = len

    def call(self, x):
        positions = tf.range(start=0, limit=self.maxlen, delta=1)
        positions = self.pos_emb(positions)
        return x + positions


def get_TRANSFORMER(shape=(32, 20)):
    input = layers.Input(name="example", shape=(shape[0], shape[1]))
    x = tf.keras.layers.Normalization(axis=1)(input)
    # labels = layers.Input(name="label", shape=(shape[0],))
    x = Dense(64, activation="relu")(x)
    x = TokenAndPositionEmbedding(len=32, dim=64)(x)
    x = TransformerBlock(64, 5, 128)(x)
    x = TransformerBlock(64, 5, 128)(x)
    x = Dense(32, activation="relu")(x)
    output = Dense(3, activation="softmax", name="finish")(x)

    # output = LogisticEndpoint(name="binary_crossentropy")(labels, x)

    model = tf.keras.models.Model(inputs=input, outputs=output, name="fraud_detector")
    return model
