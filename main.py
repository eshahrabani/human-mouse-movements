import numpy as np
from keras.layers import Input, LSTM, Dense
from keras.models import Model


def getSequences(mouse_paths_file):
    sequences = []  # [[(x1, y1), 0.25, ..., (xn, yn)], [...]] - can have wait times interspersed
    targets = []  # [((x_start, y_start), (x_end, y_end))] - represents target for each sequence
    with open(mouse_paths_file, 'r') as f:
        current_sequence = []
        for line in f:
            fields = line.split(' ')
            if fields[0] == 'begin':
                current_sequence = []  # just to make sure
                x1 = int(fields[1])
                y1 = int(fields[2])

                x2 = int(fields[3])
                y2 = int(fields[4])
                targets.append([(x1, y1), (x2, y2)])
            elif fields[0] == 'move':
                x = int(fields[1])
                y = int(fields[2])
                current_sequence.append((x, y))
            elif fields[0] == 'wait':
                wait_time = float(fields[1])
                current_sequence.append(wait_time)
            elif fields[0].rstrip() == 'end':
                sequences.append([current_sequence])
                current_sequence = []
    # sanity check
    assert len(sequences) == len(targets)
    return sequences, targets


sequences, targets = getSequences('encoding.txt')

coord_target_input = Input(shape=(2,), dtype='int32', name='coord_target_input')




