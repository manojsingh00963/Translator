import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense
import json

# -------------------------------
# Step 1: Load Dataset
# -------------------------------
data = pd.read_csv('translations.csv')  # Must contain 'source' & 'target' columns

# -------------------------------
# Step 2: Preprocess Data
# -------------------------------
source_texts = data['source'].astype(str).tolist()
# Add <start> and <end> around target
target_texts = [f'<start> {t} <end>' for t in data['target'].astype(str).tolist()]

# Tokenizers
source_tokenizer = Tokenizer(oov_token="<OOV>")
source_tokenizer.fit_on_texts(source_texts)

target_tokenizer = Tokenizer(oov_token="<OOV>")
target_tokenizer.fit_on_texts(target_texts)

# (Optional) Save tokenizers
with open('source_tokenizer.json', 'w') as f:
    f.write(json.dumps(source_tokenizer.to_json()))

with open('target_tokenizer.json', 'w') as f:
    f.write(json.dumps(target_tokenizer.to_json()))

# Convert texts to sequences
source_sequences = source_tokenizer.texts_to_sequences(source_texts)
target_sequences = target_tokenizer.texts_to_sequences(target_texts)

# Determine max lengths & pad
max_source_length = max(len(seq) for seq in source_sequences)
max_target_length = max(len(seq) for seq in target_sequences)

padded_source = pad_sequences(source_sequences, maxlen=max_source_length, padding='post')
padded_target = pad_sequences(target_sequences, maxlen=max_target_length, padding='post')

# Vocabulary sizes
source_vocab_size = len(source_tokenizer.word_index) + 1
target_vocab_size = len(target_tokenizer.word_index) + 1

# -------------------------------
# Step 3: Build the Seq2Seq Model
# -------------------------------
embedding_dim = 256
units = 512

# --- Encoder ---
encoder_inputs = Input(shape=(max_source_length,))
encoder_embedding = Embedding(source_vocab_size, embedding_dim)(encoder_inputs)
encoder_lstm, state_h, state_c = LSTM(units, return_state=True)(encoder_embedding)
encoder_states = [state_h, state_c]

# --- Decoder ---
# NOTE: The decoder expects sequences of length (max_target_length - 1)
decoder_inputs = Input(shape=(max_target_length - 1,))
decoder_embedding_layer = Embedding(target_vocab_size, embedding_dim)
decoder_embedded = decoder_embedding_layer(decoder_inputs)

decoder_lstm_layer = LSTM(units, return_sequences=True, return_state=True)
decoder_lstm_outputs, _, _ = decoder_lstm_layer(decoder_embedded, initial_state=encoder_states)

decoder_dense = Dense(target_vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_lstm_outputs)

# Combined Model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# -------------------------------
# Step 4: Prepare Training Data
# -------------------------------
# Teacher forcing: shift target by 1
y_input = padded_target[:, :-1]  # shape => (batch_size, max_target_length - 1)
y_output = padded_target[:, 1:]  # shape => (batch_size, max_target_length - 1)

# Keras expects outputs to have an extra dimension for sparse targets
y_output = np.expand_dims(y_output, axis=-1)

# -------------------------------
# Step 5: Train the Model
# -------------------------------
model.fit(
    [padded_source, y_input],
    y_output,
    batch_size=64,
    epochs=20,
    validation_split=0.2
)

# -------------------------------
# Step 6: Save the Model
# -------------------------------
model.save('multi_language_translator.h5')
print("Training complete. Model and tokenizers saved.")
