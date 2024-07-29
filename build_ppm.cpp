import numpy as np
import graphviz
from collections import defaultdict, Counter

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
        context = sequence[max(0, i - D):i]
        symbol = sequence[i]
        trie.insert(context, symbol)
    return trie

def compute_probabilities(trie, D):
    probabilities = {}
    nodes = [(trie.root, "")]
    while nodes:
        node, context = nodes.pop()
        total = sum(child.count for child in node.children.values())
        if total > 0:
            probabilities[context] = {symbol: child.count / total for symbol, child in node.children.items()}
        for symbol, child in node.children.items():
            nodes.append((child, context + symbol))
    return probabilities

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
    return dot

# Test the algorithm on the sequence "abracadabra"
sequence = "abracadabra"
D = 3  # Set context size
trie = construct_trie(sequence, D)
probabilities = compute_probabilities(trie, D)
dot = visualize_trie(trie)

# Display the probabilities
for context, probs in probabilities.items():
    print(f"Context: '{context}' -> {probs}")

# Render the trie visualization
dot.render('trie', format='png', view=True)
