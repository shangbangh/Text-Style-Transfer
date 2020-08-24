'''
Created on May 29, 2020

@author: myuey
'''

from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding
from keras.callbacks import ModelCheckpoint
from keras import models
import numpy as np
from util import analysis1

#data source folders
machFolder = "./machB0/"
humFolder = "./humTagB0/"
#data source files
machData = "B0_M.txt"
humData = "B0_tag.txt"
#create lists of data
mach_list = analysis1.wordlist(machFolder)
hum_list = analysis1.wordlist(humFolder)
#get vocabulary from input files
machVocab = analysis1.vocab(machFolder)
humVocab = analysis1.vocab(humFolder)
#analysis1.write_list(humVocab, "debug.txt")
input_words = sorted(list(machVocab))
target_words = sorted(list(humVocab))
num_encoder_tokens = len(machVocab)
num_decoder_tokens = len(humVocab)
#create dictionaries
input_token_index = dict(
    [(word, i) for i, word in enumerate(input_words)])
target_token_index = dict(
    [(word, i) for i, word in enumerate(target_words)])

#encoder input data will be machine translated chapters
#decoder input data will be human translated chapters
chap_quant = len(mach_list) #number of chapters inside data files
max_length_in = analysis1.folder_max_word(machFolder) #max number of words in a machine chapter
max_length_out = analysis1.folder_max_word(humFolder) #max number of words in a human chapter

encoder_input_data = np.zeros((chap_quant, max_length_in), dtype='float32')
decoder_input_data = np.zeros((chap_quant, max_length_out), dtype='float32')
decoder_target_data = np.zeros((chap_quant, max_length_out, num_decoder_tokens), dtype='float32')

#fill data
for i, (input_text, target_text) in enumerate(zip(mach_list, hum_list)):
    for t, word in enumerate(analysis1.getTokens(input_text)):
        encoder_input_data[i, t] = input_token_index[word]
        
    for t, word in enumerate(analysis1.getTokens(target_text)):
        # decoder_target_data is ahead of decoder_input_data by one timestep
        decoder_input_data[i, t] = target_token_index[word]
        
        if t > 0:
            # decoder_target_data will be ahead by one timestep
            # and will not include the start character.
            decoder_target_data[i, t - 1, target_token_index[word]] = 1.

#build encoder model
embed_size = 50

encoder_inputs = Input(shape=(None,))
en_x=  Embedding(num_encoder_tokens, embed_size)(encoder_inputs)
encoder = LSTM(embed_size, return_state=True)
encoder_outputs, state_h, state_c = encoder(en_x)
# Discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# decoder model, using `encoder_states` as initial state.

decoder_inputs = Input(shape=(None,))

dex=  Embedding(num_decoder_tokens, embed_size)

final_dex= dex(decoder_inputs)


decoder_lstm = LSTM(embed_size, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(final_dex, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

resume = True
baseFolder = "./SavedModels/"
loadFolder = "./EndModels/"
if(resume):
    model = models.load_model(loadFolder + "model-1000-1.9298.hdf5")
else:
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

filepath= baseFolder + "model-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, save_weights_only=False, mode='min')
callbacks_list = [checkpoint]

model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=128,
          epochs=1000,
          validation_split=0.05, callbacks=callbacks_list)

encoder_model = Model(encoder_inputs, encoder_states)

#sampling model
decoder_state_input_h = Input(shape=(50,))
decoder_state_input_c = Input(shape=(50,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

final_dex2= dex(decoder_inputs)

decoder_outputs2, state_h2, state_c2 = decoder_lstm(final_dex2, initial_state=decoder_states_inputs)
decoder_states2 = [state_h2, state_c2]
decoder_outputs2 = decoder_dense(decoder_outputs2)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs2] + decoder_states2)

# Reverse-lookup token index to decode sequences back to
# something readable.
reverse_input_char_index = dict(
    (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
    (i, char) for char, i in target_token_index.items())

def translate(input_seq):
    #encode input as state vectors
    states_value = encoder_model.predict(input_seq)
    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1,1))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = target_token_index['START_']
    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_str = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_str += ' '+sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '_END'):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = [h, c]

    return decoded_str
