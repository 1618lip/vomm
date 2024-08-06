import math 
import numpy as np
import re
from music21 import chord, harmony, pitch
from itertools import combinations
import sys


def note_to_frequency(note_name):
    # Create a Pitch object from the note name
    p = pitch.Pitch(note_name)
    # Get the frequency of the pitch
    frequency = round(p.frequency)
    return frequency

def chordToNotes(chord_name):
    try:
        # Create a ChordSymbol object from the chord name
        chord_symbol = harmony.ChordSymbol(chord_name)
        # Get the pitches of the chord
        pitches = chord_symbol.pitches
        # Convert pitches to note names
        note_names = [note_to_frequency(p.nameWithOctave) for p in pitches]
        return note_names
    except Exception as e:
        print(f"Error processing chord '{chord_name}': {e}")
        return []

def readFile(file_path):
    sections = []
    with open(file_path, 'r') as file:
        text = file.read()
        # Initialize an empty list to store the sections

        # Split the text by lines and process each line
        for line in text.splitlines():
            if not line.startswith("A") and not line.startswith("B"):
                # Split the line into chord groups and process each group
                chords = line.strip("[], ").split("], [")
                for chord_group in chords:
                    # Split each chord group into individual chords and add to sections
                    c = chord_group.split(", ")
                    
                    # for i in range(0,len(c)):
                    #     c[i]= chordToNotes(c[i])
                    for x in c:    
                        sections.append(x)
    return sections
# def prettyPrint(nested_list):
#     """
#     Pretty prints the nested list in a readable format.
#     """
#     with open('piano_frequency.txt', 'w') as f:
#         for section in nested_list:
#             #f.write("[\n")
#             for bar in section:
#                 formatted_bar = ", ".join(f'{note}' for note in bar)
#                 if (re.search("[A-C], [1-3]", formatted_bar)):
#                     str = ""
#                     for note in bar:
#                         str = str + note
#                     f.write(str+"\n")
#                     continue
#                 f.write(f"  {formatted_bar}\n")
#             f.write("\n")