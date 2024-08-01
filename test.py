# from music21 import converter, note, stream, pitch, harmony, chord
# import matplotlib.pyplot as plt
# import math, re
# from itertools import combinations
# import sys

# def partition_measure(measure, num_partitions=1):  # split each measure into 4 beats
#     measure_duration = measure.duration.quarterLength
#     partition_length = measure_duration / num_partitions
#     partitions = []
#     for i in range(num_partitions):
#         start_offset = i * partition_length
#         end_offset = (i + 1) * partition_length
#         partitions.append((start_offset, end_offset))
#     return partitions

# def extract_elements_in_range(measure, start_offset, end_offset):
#     elements_in_range = []
#     for element in measure.flatten().notesAndRests.getElementsByOffset(start_offset, end_offset, includeEndBoundary=False):
#         if isinstance(element, (note.Note, note.Rest)):  # Include both notes and rests
#             elements_in_range.append(element)
#     return elements_in_range


import sys
from fractions import Fraction
from music21 import converter, note, tempo

def partition_measure(measure):
    # Implement partition logic if needed
    return [(0, measure.duration.quarterLength)]

def extract_elements_in_range(measure, start_offset, end_offset):
    # Extract elements within the given offset range
    elements = []
    for el in measure.elements:
        if el.offset >= start_offset and el.offset < end_offset:
            elements.append(el)
    return elements

file_path = str(sys.argv[1])
score = converter.parse(file_path)

# Extract notes and partition measure
for part in score.parts:
    melody = ""
    for measure in part.getElementsByClass('Measure'):
        measure_number = measure.measureNumber
        partitions = partition_measure(measure)
        for i, (start_offset, end_offset) in enumerate(partitions):
            section_elements = extract_elements_in_range(measure, start_offset, end_offset)
            
            for el in section_elements:
                if isinstance(el, note.Note):
                    midi_number = el.pitch.midi
                    
                    melody += str(midi_number)+":"+str(int(el.quarterLength*12))+":"
                elif isinstance(el, note.Rest):
                    
                    melody += "0:"+str(int(el.quarterLength*12))+":"

    break

print(melody)

"""
| Note Type                  | Value |
|----------------------------|-------|
| Whole note (semibreve)     | 48    |
| Half note (minim)          | 24    |
| Quarter note (crotchet)    | 12    |
| Eighth note (quaver)       | 6     |
| Sixteenth note (semiquaver)| 3     |
| Quarter note triplet       | 8     |
| Eighth note triplet        | 4     |
| Sixteenth note triplet     | 2     |

Using these values, we can represent all note lengths without decimals.
"""