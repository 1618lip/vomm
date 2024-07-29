import numpy as np
import graphviz
from collections import defaultdict, Counter
import os
import sys
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

alphabet = [':']
for i in range(0, 10):
    alphabet.append(str(i))

class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, context, symbol):
        node = self.root
        for char in context:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        if symbol not in node.children:
            node.children[symbol] = TrieNode()
        node.children[symbol].count += 1

    def get_counts(self, context):
        node = self.root
        for char in context:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.children

def construct_trie(sequence, D):
    trie = Trie()
    n = len(sequence)
    for i in range(n):
        context = sequence[max(0, i - D):i]  # if i-D < 0, that means context length is less than D
        symbol = sequence[i]
        trie.insert(context, symbol)
    return trie

def get_contexts(training_data, D):
    contexts = set()
    N = len(training_data)
    for k in range(1, D + 1):
        contexts = contexts.union([training_data[t:t + k] for t in range(N - k + 1)])
    return sorted(contexts)

def unique_symbols(training_data):
    sym = set()
    for c in training_data:
        sym = sym.union([c])
    return sym

def count_occurrences(training_data, D):
    contexts = get_contexts(training_data, D)
    counts = {context: {sigma: 0 for sigma in unique_symbols(training_data)} for context in contexts}
    N = len(training_data)
    for i in range(1, D + 1):
        for j in range(0, N - i):
            s = training_data[j:j + i]
            sigma = training_data[j + i]
            counts[s][sigma] += 1
    return counts

def compute_probabilities_with_escape(counts, D):
    probabilities = {}
    all_symbols = unique_symbols("".join(counts.keys()))  # Get the complete alphabet from the contexts
    for context, symbols in counts.items():
        total_counts = sum(symbols.values())
        num_symbols = len([sigma for sigma in symbols if symbols[sigma] > 0])
        if total_counts + num_symbols == 0:
            probabilities[context] = {sigma: 1 / len(all_symbols) for sigma in all_symbols}
            continue
        probabilities[context] = {}
        for sigma in all_symbols:
            if symbols[sigma] > 0:
                probabilities[context][sigma] = symbols[sigma] / (total_counts + num_symbols)
            else:
                shorter_context = context[1:]  # Shorten the context
                if shorter_context in probabilities:
                    probabilities[context][sigma] = probabilities[shorter_context][sigma] * \
                                                    (num_symbols / (total_counts + num_symbols))
                else:
                    probabilities[context][sigma] = 1 / len(all_symbols)  # Base case for empty context
        probabilities[context]['escape'] = num_symbols / (total_counts + num_symbols)
    return probabilities

def print_probabilities(probabilities):
    for context, symbols in probabilities.items():
        for sigma, prob in symbols.items():
            if sigma == 'escape':
                print(f"P(escape|{context}) = {prob}")
            else:
                print(f"P({sigma}|{context}) = {prob}")
                
def visualize_trie(trie):
    dot = graphviz.Digraph()
    nodes = [(trie.root, "")]
    idx = 0
    node_ids = {trie.root: str(idx)}
    dot.node(str(idx), "root")
    while nodes:
        node, context = nodes.pop()
        parent_id = node_ids[node]
        for symbol, child in node.children.items():
            idx += 1
            child_id = str(idx)
            node_ids[child] = child_id
            dot.node(child_id, f"{context + symbol} ({child.count})")
            dot.edge(parent_id, child_id, label=symbol)
            nodes.append((child, context + symbol))
            #idx += 1
    return dot
def traverse_path(trie, path):
    node = trie.root
    counters = []
    for char in path:
        if char in node.children:
            node = node.children[char]
            counters.append((char, node.count))
        else:
            return None  # Path does not exist in the trie
    return counters

def context_children_and_counters(trie, context, symbol):
    node = trie.root
    for char in context:
        node = node.children[char]
    end_of_context = node
    total = 0 
    for child in node.children:
        if child == symbol:
            continue # UNCOMMENT THIS IF STATEMENT IF YOU DON'T WANT TO USE THE EXCLUSION MECHANISM
        total += child.count
    toReturn = (len(node.children), total)
    return toReturn 


def compute_ppm(counts, training_data, D):
    probs = counts # same format, but just change the value from counts to probability
    for s in get_contexts(training_data, D):
        for sigma in unique_symbols(training_data):
            counters = traverse_path(trie, s+sigma)
            context_children_count = context_children_and_counters(trie, s)[0]
            total_counters = context_children_and_counters(trie, s)[1]
            if counters != None:
                #NOT ESCAPE
                sigma_count = counters[-1][1]
                probs[s][sigma] = (sigma_count) / (context_children_count + total_counters)
            else:
                #ESCAPE & EXCLUSION
                p_escape = 
                probs[s][sigma] = 
            
# Test the algorithm on the sequence "0:333:0:167:63:83:"
sequence = sys.argv[2]
D = int(sys.argv[1])  # Set context size
counts = count_occurrences(sequence, D)
trie = construct_trie(sequence, D)
probabilities_with_escape = compute_probabilities_with_escape(counts, D)
print_probabilities(probabilities_with_escape)
dot = visualize_trie(trie)
# Display the nodes with counters
# print("Nodes with counters:")
# for node in nodes_with_counters:
#     print(node)
print(count_occurrences(sequence, D))
# Render the trie visualization
dot.render('trie', format='png', view=True)
#print(count_occurrences(sequence, D))