import sys
import math as m
from vomm_ppm import count_occurrences, compute_ppm
from get_chords import readFile
from createdistribution import createDistribution
import matplotlib.pyplot as plt
"""
Perform sliding analysis. Window length is W >> D.

Heuristic constraints: L >> kW, where k is in an even positive integer. And W > 4D
"""
D = int(sys.argv[1])
W = 12*int(sys.argv[2]) # num beats
alphabet = [':']
for i in range(0, 10):
    alphabet.append(str(i))
# def avg_log_loss(probs, test, D):
#     context = ""
#     #print(probs[''][test[0]])
#     total = m.log2(probs[''][test[0]])
#     for i in range(1,D+1):
#         total += m.log2(probs[test[0:i]][test[i]])
#     for i in range(1, len(test)-D):
#         context = test[i:i+D]
#         sigma = test[i+D]
#         total += m.log2(probs[context][sigma])
#     total = -total / len(test)
#     return total
# def sliding_window(Q, D, probs, start, end):
#     copy = Q
#     cum_time = 0
#     for i in range(0, len(Q)):
       


# windows = [0] *  (len(sequence)-2*W)
# for i in range(0, len(sequence)-2*W):
#     windowed = sequence[i:i+W]
#     #print(windowed)
#     probss = compute_ppm(counts, windowed, D)
#     tests = sequence[i+W:i+2*W]
#     #print(tests)
#     windows[i] = avg_log_loss(probss, tests, D)

def get_notes(Q):
    return [int(Q[2*i]) for i in range(0, len(Q)//2)]
def map_to_piano_range(value):
    """
    Maps a value from the range 10-97 to the range 21-108

    Parameters:
    value (int): The value to be mapped.

    Returns:
    int: The mapped value in the new range.
    """
    if value < 10 or value > 98:
        raise ValueError("Value should be between 10 and 97")
    return value + 10
    
def chord_of_note(chords, Q):
    """
    |0 12 24 36 |48 60 72 84 |96
    """
    copy_Q = Q
    cum_time = 0
    chord_note_pos = []
    for i in range(0, len(chords)):
        while 12*i <= cum_time and cum_time < 12*(i+1):
            note = copy_Q.pop(0)
            dur = int(copy_Q.pop(0))
            if int(note) == 10:
                lmi = 0
            else:
                lmi = round(m.log2(11*createDistribution(chords[i], map_to_piano_range(int(note)))),2)
            chord_note_pos.append((note, chords[i], cum_time, dur, lmi))
            cum_time += dur
    return chord_note_pos

def sliding_window(chords, Q, window):
    note_info = chord_of_note(chords, Q)
    final = []
    for k in range(0, len(note_info)):
        note_in_window = []
        test_sequence = []
        for i in range(0, len(note_info)):
            if (12*k <= int(note_info[i][2]) and 12*k+window > note_info[i][2]) or (12*k - note_info[i][3] <= int(note_info[i][2]) and 12*k+window > note_info[i][2]):
                note_in_window.append(note_info[i])
            elif  (12*k + window <= int(note_info[i][2]) and 12*k+2*window > note_info[i][2]) or (12*k +window - note_info[i][3] <= int(note_info[i][2]) and 12*k+2*window > note_info[i][2]):
                test_sequence.append(note_info[i])
        if test_sequence == []:
            break
        final.append((note_in_window, test_sequence))
        
    return final

def read_sliding_window(slides):
    for pair in slides:
        print(f"\nTraining: {pair[0]} \n Test: {pair[1]}\n")

f = open("solo_representation.txt", "r") 
q = f.read()
Q = list(q.split(":"))
Q.pop()

#print(chord_of_note(readFile("yardbird_suite_parsed.txt"), Q))

def average_log_loss(training_and_test, a=0.4):
    toReturn = []
    count = 0
    for pair in training_and_test:
        training, test = pair
        
        training_sequence = ""
        test_sequence = ""
        for x in training:
            training_sequence = training_sequence + str(x[0]) + ":" + str(x[3]) + ":"
        for y in test:
            test_sequence = test_sequence + str(y[0]) + ":" + str(y[3]) + ":"
        # print(training_sequence)
        # print(test_sequence)
        counts = count_occurrences(training_sequence, D)
        counts_test = count_occurrences(test_sequence, D)
        counts_test.update(counts)
        for context in counts_test:
            if context not in counts:
                counts_test[context] = {sigma: 0 for sigma in alphabet}
        #print(counts_test)

        probs = compute_ppm(counts_test, training_sequence, D)
        
        # TODO: Think of how exactly to do the average log loss AND involve the LMI value. 

        # Let's try by just doing P(xT|x1...x(T-1)) and then for each P(note, dur|context), add the lmi.
        context = ""
        total = 0
        for n in test:  
            # probs[context][":"]*(1+a*n[4])
            context = context[max(0,len(context)-D):]
            
            #context += n[0]+":"+n[3] 
            prob_of_note = probs[context][str(n[0][0])] if probs[context][str(n[0][0])] != 0 else 1/len(alphabet)
            #total += m.log2(prob_of_note)
            context+=str(n[0][0])
            context = context[max(0,len(context)-D):]
            
            prob_of_note *= probs[context][str(n[0][1])] if probs[context][str(n[0][1])] != 0 else 1/len(alphabet)
            #total += m.log2(prob_of_note)
            context+=str(n[0][1])
            context = context[max(0,len(context)-D):]
          
            prob_of_note *= probs[context][':'] if probs[context][':'] != 0 else 1/len(alphabet)
            #total += m.log2(prob_of_note)
            
            context += ':'
            context = context[max(0,len(context)-D):]
         
            if len(str(n[3])) > 1:
                
                prob_of_note *= probs[context][str(n[3])[0]] if probs[context][str(n[3])[0]] != 0 else 1/len(alphabet)
                #total += m.log2(prob_of_note)
                context+=str(str(n[3])[0])
                context = context[max(0,len(context)-D):]
                prob_of_note *= probs[context][str(n[3])[1]] if probs[context][str(n[3])[1]] != 0 else 1/len(alphabet)
                #total += m.log2(prob_of_note)
                context+=str(str(n[3])[1])
                context = context[max(0,len(context)-D):]        
            else:
                prob_of_note *= probs[context][str(n[3])] if probs[context][str(n[3])] != 0 else 1/len(alphabet)
                #total += m.log2(prob_of_note)
                context+=str(n[3])
                context = context[max(0,len(context)-D):]
        
            prob_of_note *= probs[context][':'] if probs[context][':'] != 0 else 1/len(alphabet)
            prob_of_note = prob_of_note*(1+a*int(n[4]))
            
            context += ":"
            context = context[max(0,len(context)-D):]
            
                
            total += m.log2(prob_of_note)
            #count += 1
            #print(count)
        # total = m.log2(probs[''][test[0]])
        # for i in range(1,D+1):
        #     total += m.log2(probs[test[0:i]][test[i]])
        # for i in range(1, len(test)-D):
        #     context = test[i:i+D]
        #     sigma = test[i+D]
        #     total += m.log2(probs[context][sigma])
        total = -total / len(test)
        toReturn.append(total)
        
        
    return toReturn
#print(windows)
#read_sliding_window(sliding_window(readFile("yardbird_suite_parsed.txt"), Q, W))

def plot_numbers_over_time(numbers):
    """
    Plots an array of numbers over time.

    Parameters:
    numbers (list or array): Array of numbers to be plotted.
    """
    # Generate a list of time points (e.g., 0, 1, 2, 3, ...)
    time_points = []
    x = 2
    for i in range(0, len(numbers)):
        time_points.append(x)
        x += 0.25
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, numbers, marker='o', linestyle='-')

    # Add labels and title
    plt.xlabel('Measure')
    plt.ylabel('Average Log Loss')
    plt.title('Melodic Complexity')

    # Add grid for better readability
    plt.grid(True)

    # Display the plot
    plt.show()
plot_numbers_over_time(average_log_loss(sliding_window(readFile("Control3_parsed.txt"), Q, W)))