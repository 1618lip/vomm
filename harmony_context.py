import xml.etree.ElementTree as ET
from sklearn.metrics import log_loss
import random 
from xml.dom import minidom
import zipfile
import os
import mido # type: ignore
import sys
from mido import MidiFile, MidiTrack, Message # type: ignore
import time

start = time.time()
tempo = sys.argv[2]
q = sys.argv[1]
Q = q.split(":")

length_16th_note = (25 * tempo) / 6

def duration_to_position(tau):
    
print(Q)
end = time.time()
print(end - start)

