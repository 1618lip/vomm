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
q = sys.argv[1]
Q = list(q.split(":"))
Q.pop()
"""
Q will be like [note1, dur1, note2, dur2, ...]
Get the (i+1)th note = Q[2i]
Get the (i+1)th dur = Q[2i+1]

"""
cum_time = 0 # Start of song
weights  = [1] * (len(Q) // 2)
"""
We propose that the downbeats are in beat 1 and 3 (2 and 4 are not really). 
Let b = 12

->       || # . #  .  | #  .  #  .  ||  
cum_time || 0 b 2b 3b | 4b 5b 6b 7b ||   <-- cum_time

if the cum_time mod 48 = 0 OR 24, then it is downbeat. 

"""
for i in range(0, len(Q) // 2):
    if cum_time % 48 == 0: 
        weights[i] = 1.2 # First
    elif cum_time % 48 == 24:
        weights[i] = 1.1
    cum_time += int(Q[2*i+1])
# def duration_to_position(Q):
#     ru
print(Q)
print(weights)
end = time.time()
print(f"Time elapsed = {end - start} seconds")

