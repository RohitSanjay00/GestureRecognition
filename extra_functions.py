import numpy as np
import os

class extra_functions:
    label_map = None
    sequences = []
    labels = []
    def __init__(self, no_sequence, sequence_length, data_path, actions):
        self.no_sequence = no_sequence
        self.sequence_length = sequence_length
        self.data_path = data_path
        self.actions = actions
    
    def make_folders(self):
        data_path = os.path.join(self.data_path)
        actions = np.array(self.actions)
        for action in actions:
            for sequence in range(self.no_sequence):
                try: 
                    os.makedirs(os.path.join(self.data_path, action, str(sequence)))
                except:
                    pass
    def return_no_sequence(self):
        return self.no_sequence
    def return_sequence_length(self):
        return self.sequence_length
    def creating_label_map(self):
        self.label_map = {label:num for num, label in enumerate(self.actions)}
    def return_label_map(self):
        return self.label_map
    def concating_gesture_sequences(self, path, no_sequence, sequence_length, actions, label_map):
        sequences, labels = [],[]
        for action in actions:
            for sequence in range(no_sequence):
                window=[]
                for frame_num in range(sequence_length):
                    if frame_num == sequence_length:
                        break
                    else:
                        res = np.load(os.path.join(path, action, str(sequence), "{}.npy".format(frame_num)))
                        res = res.flatten()
                        #print(res.shape)
                        window.append(res)
                sequences.append(window)
                labels.append(label_map[action])
        return sequences, labels
            





    