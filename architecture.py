import re
from collections import defaultdict

# Markov chain
def scan_weights(child, weights, index, tree):
    weights[tree.identifier][child.identifier] = weights[tree.identifier][child.identifier] + 1
    for subitem in tree.children:
        # weights[child.identifier][subitem.identifier] = weights[child.identifier][subitem.identifier] + 1
        weights[subitem.identifier][child.identifier] = weights[subitem.identifier][child.identifier] + 1
        scan_weights(subitem, weights, index, subitem)

def markov(index, tree):
    weights=defaultdict(lambda: defaultdict(int))
    for child in tree.children:
        scan_weights(child, weights, index, tree)
    return weights

class Atom:
    def __init__(self, label, identifier):
        self.label = label
        self.identifier = identifier
        self.children = []
    def __repr__(self):
        return self.label
class Node:
    def __init__(self, identifier):
        self.children = []
        self.identifier = identifier
    def append(self, node):
        self.children.append(node)
    def add_atom(self, atom, identifier):
        atom = Atom(atom, identifier)
        self.children.append(atom)
        return atom
    def __repr__(self):
        string = "("
        for child in self.children:
            string += str(child) + " "
        string += ")"
        return string
        
class Parser:
    def __init__(self, text):
        self.text = text
        self.last_char = " "
        self.pos = 0
        self.end = False
        
    def getchar(self):
        token = self.text[self.pos]
        if self.pos + 1 == len(self.text):
            self.end = True

            return token
        self.pos = self.pos + 1
        
        return token
    
    def gettok(self):
        while (self.end == False and (self.last_char == " " or self.last_char == "\n")):
            self.last_char = self.getchar()
            
            
        if self.last_char == "(":
            self.last_char = self.getchar()
            return "open"
        if self.last_char == ")":
            self.last_char = self.getchar()
            return "close"
        
        if re.match("[a-zA-Z0-9\.\_\-]+", self.last_char):
            identifier = ""
            while self.end == False and re.match("[a-zA-Z0-9\.\_\-]+", self.last_char):
                
                identifier = identifier + self.last_char
                self.last_char = self.getchar()
            
            if self.end and self.last_char != ")" and self.last_char != "\n":
                identifier += self.last_char
            
            return identifier.lower()
        
        return
        
            
    def parse(self):
        stack = []
        token = self.gettok()
        lastpopped = None
        identifier = 0
        index = {}
        while not self.end:
            print(token)
            if token == "open":
                item = Node(identifier)
                index[identifier] = item
                if len(stack) == 0:
                    stack.append(item)
                else:
                    
                    
                    stack[-1].append(item)
                    stack.append(item)
            elif token == "close":
                lastpopped = stack.pop()
            else:
                atom = stack[-1].add_atom(token, identifier)
                index[identifier] = atom
            token = self.gettok()
            identifier = identifier + 1
        return stack[-1], index

def parse_tree(text):
    parser = Parser(text)
    tree = parser.parse()
    print(tree)
    return tree

architecture = """
(load-balancer 1 (web 1 (database)))
"""
tree, index = parse_tree(architecture)
weights = markov(index, tree)
def print_weights(weights, index):
    for key, value in weights.items():
        for key2, value2 in value.items():
            print("{} -> {} (strength {})".format(index[key], index[key2], value2))
print_weights(weights, index)
