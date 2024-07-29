import numpy as np
import scipy.stats as stats
from collections import defaultdict
import mido
from mido import MidiFile, MidiTrack, Message
import music21
import sys

def find_elbow(S):
    Sp = S - S[0]
    N = Sp.shape[0] - 1
    SN = Sp[-1]
    M = SN / N
    R = (SN**2 + N**2)**0.5
    sintheta = SN / R
    costheta = N / R
    x = np.arange(Sp.shape[0])
    y = Sp
    yp = y * costheta - x * sintheta
    yp = np.abs(yp)
    elbow = yp.argmax()
    return elbow

def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (stats.entropy(P, M) + stats.entropy(Q, M))

def find_contexts(training_data, d=4):
    contexts = set()
    N = len(training_data)
    for k in range(1, d + 1):
        contexts = contexts.union([training_data[t:t + k] for t in range(N - k + 1)])
    return contexts

def count_occurrences(training_data, d=4, alphabet_size=None):
    contexts = find_contexts(training_data, d=d)
    if alphabet_size is None:
        alphabet_size = max(note for note, _ in training_data) + 1
    counts = dict([(x, np.zeros(alphabet_size, dtype=int)) for x in contexts])
    counts[()] = np.bincount([note for note, _ in training_data], minlength=alphabet_size)
    N = len(training_data)
    for k in range(1, d + 1):
        for t in range(N - k):
            s = training_data[t:t + k]
            sigma = training_data[t + k][0]
            counts[s][sigma] += 1
    return counts

def compute_ppm_probability(counts):
    d = max([len(x) for x in counts.keys()])
    alphabet_size = counts[()].shape[0]
    pdf = dict([(x, np.zeros(alphabet_size)) for x in counts.keys()])
    byk = [[] for k in range(d + 1)]
    for x in counts.keys():
        byk[len(x)].append(x)
    pdf[()] = (counts[()] + 1.0) / (counts[()].sum() + alphabet_size)
    for k in range(1, d + 1):
        for x in byk[k]:
            sigma_observed = np.argwhere(counts[x] > 0).reshape(-1)
            alphabet_obs_size = len(sigma_observed)
            sigma_escaped = np.argwhere(counts[x] == 0).reshape(-1)
            denominator = alphabet_obs_size + counts[x].sum()
            x_1 = x[1:]
            escape_factor = alphabet_obs_size * 1.0 / denominator if alphabet_obs_size > 0 else 1.0
            pdf[x][sigma_observed] = counts[x][sigma_observed] * 1.0 / denominator
            if len(sigma_escaped) > 0:
                pdf[x][sigma_escaped] = escape_factor * pdf[x_1][sigma_escaped] / pdf[x_1][sigma_escaped].sum()
            pdf[x] = pdf[x] / pdf[x].sum()
    return pdf

def find_largest_context(chunk, fast_lookup_table, d):
    if len(chunk) == 0:
        return ()
    current_context = ()
    end = len(chunk)
    start = end
    while chunk[start:end] == current_context:
        start -= 1
        #print([p in fast_lookup_table[current_context] for p in chunk[start:end]])
        midi_arr = []
        print(fast_lookup_table[current_context])
        for tup in fast_lookup_table[current_context]:
            midi_arr.append(tup[0][0])
        #print(midi_arr)
        if start < 0 or start < end - d:
            break
        if all([p in midi_arr for p in chunk[start:end]]):
            current_context = chunk[start:end]
        else:
            break
    return current_context

class ppm:
    def __init__(self):
        pass

    def generate_fast_lookup(self):
        context_by_length = dict([(k, []) for k in range(self.d + 1)])
        for x in self.pdf_dict.keys():
            context_by_length[len(x)].append(x)
        self.context_child = {}
        for k in range(self.d):
            for x in context_by_length[k]:
                self.context_child[x] = [y for y in context_by_length[k + 1] if y[1:] == x]
        for x in context_by_length[self.d]:
            self.context_child[x] = []

    def fit(self, training_data, d=4, alphabet_size=None):
        if alphabet_size is None:
            alphabet_size = max(note for note, _ in training_data) + 1
        self.alphabet_size = alphabet_size
        self.d = d
        counts = count_occurrences(tuple(training_data), d=self.d, alphabet_size=self.alphabet_size)
        self.pdf_dict = compute_ppm_probability(counts)
        self.logpdf_dict = dict([(x, np.log(self.pdf_dict[x])) for x in self.pdf_dict.keys()])
        self.generate_fast_lookup()
        return

    def logpdf(self, observed_data):
        temp = tuple(observed_data)
        logprob = 0.0
        for t in range(len(temp)):
            chunk = temp[max(t - self.d, 0):t]
            sigma = temp[t][0]
            context = find_largest_context(chunk, self.context_child, self.d)
            logprob += self.logpdf_dict[context][sigma]
        return logprob

    def generate_data(self, prefix=None, length=200):
        if prefix is not None:
            new_data = np.zeros(len(prefix) + length, dtype=int)
            for i in range(0, len(prefix)):
                new_data[i] = prefix[i]
            start = len(prefix)
        else:
            new_data = np.zeros(length, dtype=int)
            start = 0
        for t in range(start, len(new_data)):
            chunk = tuple(new_data[max(t - self.d, 0):t])
            context = find_largest_context(chunk, self.context_child, self.d)
            new_symbol = np.random.choice(self.alphabet_size, p=self.pdf_dict[context])
            new_data[t] = new_symbol
        return new_data[start:]

    def __str__(self):
        return "\n".join(["alphabet size: %d" % self.alphabet_size,
                          "context length d: %d" % self.d,
                          "Size of model: %d" % len(self.pdf_dict)])

# Additional music-related functions
def xml_to_sequence(xml_file):
    score = music21.converter.parse(xml_file)
    sequence = []
    for part in score.parts:
        for note in part.flat.notes:
            if note.isNote:
                midi_number = note.pitch.midi
                duration = int(note.quarterLength * 480)  # Convert quarter lengths to ticks (assuming 480 ticks per quarter note)
                sequence.append((midi_number, duration))
            elif note.isRest:
                duration = int(note.quarterLength * 480)
                sequence.append((-1, duration))  # Representing rests
    return sequence

def preprocess_music(training_data):
    return [(note, duration) for note, duration in training_data]

def sequence_to_midi(sequence, output_filename):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for note, duration in sequence:
        duration_ms = int(duration)
        if note == -1:  # Handle rests
            track.append(Message('note_off', note=0, velocity=0, time=duration_ms))
        else:
            # Add note_on and note_off messages
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration_ms))
    mid.save(output_filename)

def main():
    # Convert MusicXML file to sequence
    file_name = str(sys.argv[1])
    training_sequence = xml_to_sequence(file_name)
    
    # Preprocess training data for PPM
    preprocessed_data = preprocess_music(training_sequence)
    
    # Initialize and fit PPM model
    ppm_model = ppm()
    ppm_model.fit(preprocessed_data, d=4)
    
    # Generate new musical data
    generated_data = ppm_model.generate_data(length=200)
    
    # Convert generated sequence to MIDI file
    generated_sequence = [(note, duration) for note, duration in generated_data]
    sequence_to_midi(generated_sequence, "output_midi_file.mid")
    
if __name__ == "__main__":
    main()

