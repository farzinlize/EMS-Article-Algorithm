alphabet = 'ACGT'
uniq_id = 0

class TrieNode:
    def __init__(self, label = 'U'):
        global uniq_id
        self.id = uniq_id
        uniq_id += 1
        self.childs = []
        self.label = label

    def setFather(self, father):
        self.father = father

    def isRoot(self):
        return self.label == 'R'

    def addChild(self, child):
        self.childs += [child]
        child.setFather(self)

    def labelInclude(self, char):
        for each in self.label:
            if each == char:
                return True
        return False

    def removeChild(self, child):
        newChildList = []
        for each in self.childs:
            if child.id != each.id:
                newChildList += [each]
        self.childs = newChildList

    def removeLabel(self, char):
        newLabel = ""
        for each in self.label:
            if each != char:
                newLabel += each
        self.label = newLabel

    def __str__(self):
        if self.isRoot():
            name = "Root" + str(self.id)
        else:
            name = "node" + str(self.id) + " | father:" + str(self.father.id)
        result = name  + " | childs["
        for child in self.childs:
            result += "(" + str(child.id) + ", " + child.label + "), "
        result = result[:-2] + "]"
        return result

    def copy(self):
        copyNode = TrieNode(label=self.label)
        copyNode.father = self.father
        for each in self.childs:
            copyNode.addChild(each.copy())
        return copyNode



def addMotif(currentNode, motif):
    
    # stop point - end of recursive 
    if len(motif) == 0: 
        return
    
    # motif[j] is in alphabet (isn't star character)
    if motif[0] != 'X': 

        # find child with a label containing motif[j] and add the rest of motif to it
        for child in currentNode.childs:
            if child.labelInclude(motif[0]):

                # label containing more letter (in addition to the motif[j])
                if child.label != motif[0]:

                    # making a copy of subtrie to be added as new child
                    newChild = child.copy()
                    newChild.label = motif[0]
                    child.removeLabel(motif[0])
                    currentNode.addChild(newChild)

                    # continute adding motif letters to this new child
                    return addMotif(newChild, motif[1:])
                else:

                    # continue adding motif letter to the node that its road-label contains only motif[j]
                    return addMotif(child, motif[1:])

        # there wasn't any child for motif[j] -> create one and continue 
        newChild = TrieNode(label=motif[0])
        currentNode.addChild(newChild)
        return addMotif(newChild, motif[1:])
    
    # motif[j] is star character
    else:
        
        # add rest of motif to each child
        for child in currentNode.childs:
            addMotif(child, motif[1:])

        # generate R set for new child if needed
        r = ''
        
        # each letter is condidate to be in R as T = alphabet-set 
        for char in alphabet:
            found = False
            for child in currentNode.childs:

                # if it found in any child-road label it can't be in R
                if child.labelInclude(char):
                    found = True
                    break
                
            if not found:
                r += char
            
        # R contain letters
        if len(r) != 0:

            # make a new child of u with R as its label (also add motif[1:] to it)
            newChild = TrieNode(label=r)
            currentNode.addChild(newChild)
            addMotif(newChild, motif[1:])



def printTree(root):
    print(root)
    for each in root.childs:
        printTree(each)



def intersect(u1, u2):

    # set V includes all children of u1
    V = [each for each in u1.childs]

    for v1 in V:
        for v2 in u2.childs:

            # making the intersection of labels of (u1, v1) and (u2, v2)
            newLabel = ""
            for char in v1.label:
                if char in v2.label:
                    newLabel += char

            if len(newLabel) != 0:
                if newLabel != v1.label:
                    
                    # making v1-prime copy of subtrie rooted at v1
                    v1prime = v1.copy()

                    # add as new child for u1
                    u1.addChild(v1prime)

                    # set its label
                    v1prime.label = newLabel

                    # subtract letters in new-label from edge (u1, v1)
                    for each in newLabel:
                        v1.removeLabel(each)

                    # intersect subtries rooted at v1-prime and v2
                    intersect(v1prime, v2)
                
                # two intersected labels are the same
                else:
                    intersect(v1, v2)

        # remove the subtrie rooted at v1 if it losts all of its letters (as label)
        if len(v1.label) == 0:
            u1.removeChild(v1)

    # remove the subtrie rooted at u1 if it has no more child left
    if len(u1.childs) == 0:
        if not u1.isRoot():
            f = u1.father
            f.removeChild(u1)
                    


def main():

    # subtrie presented at article as Fig.1(b) 
    print("first tree : 'XGT union AXC'")
    root1 = TrieNode(label='R')
    addMotif(root1, "XGT")
    addMotif(root1, "AXC")
    printTree(root1)
    print("###########")

    # subtrie presented at article as Fig.2(a)
    print("second tree : 'AGX union CXT'")
    root2 = TrieNode(label='R')
    addMotif(root2, "AGX")
    addMotif(root2, "CXT")
    printTree(root2)
    print("###########")

    # intercet two Motif-Trie
    intersect(root1, root2)
    print("after intersect :")
    printTree(root1)


def main_test():
    import networkx as nx
    import matplotlib.pyplot as plt

    G=nx.Graph()
    G.add_node("a")
    G.add_nodes_from(["b","c"])

    G.add_edge(1,2)
    edge = ("d", "e")
    G.add_edge(*edge)
    edge = ("a", "b")
    G.add_edge(*edge)

    G.add_edges_from([("a","c"),("c","d"), ("a",1), (1,"d"), ("a",2)])

    print("Nodes of graph: ")
    print(G.nodes())
    print("Edges of graph: ")
    print(G.edges())

    nx.draw(G)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display

def main_test2():
    a = TrieNode()
    b = TrieNode()
    print(a.id)
    print(b.id)



####################################################
main()