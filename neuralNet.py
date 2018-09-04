import random
import numpy as np
import time
import pprint
pp = pprint.PrettyPrinter()

class node(object):
    def sigmoid(self,x):
        """calculates a number's sigmoid"""
        return (1 / (1 + np.exp(-x)))
    
    def softmax(self,x):
        """takes list of numbers and returns softmaxed list"""
        return list(np.exp(x) / np.sum(np.exp(x), axis=0))
    
    def calculateActivation(self):
        if self.inputs != [] and self.mode != "OUTPUT":
            weighted_sum = 0
            for connection in self.inputs:
                weighted_sum += connection.input.outputValue * connection.weight
            weighted_sum += self.bias
            self.outputValue = self.sigmoid(weighted_sum)
        elif self.mode == "OUTPUT":
            inputs = []
            for connection in self.inputs:
                inputs.append(connection.output.outputValue * connection.weight + self.bias)
            self.outputValue = self.softmax(inputs)
        else: 
            self.outputValue = self.inputValue
    def __init__(self, mode):
        self.mode = mode
        self.bias = random.uniform(-1.0,1.0)
        self.inputValue = 0
        self.inputs = []
        self.outputs = []
        self.outputValue = 0

class layer(object):
    def __init__(self, nodes,layerNumber, mode):
        self.layerNumber = layerNumber
        self.mode = mode
        self.nodes = []

        for i in range(nodes):
            self.nodes.append(node(self.mode))

class connection(object):
    def __init__(self,inputNode,outputNode):
        self.output = outputNode
        self.input = inputNode
        self.weight = random.uniform(-1.0,1.0)

class network(object):


    
    def feedForward(self):
        self.loadInputs()
        for layer in self.layers:
            for node in layer.nodes:
                node.calculateActivation()
        output = []
        for node in self.layers[-1].nodes:
            output.append(node.outputValue)
        return max(output[0])


        
    def loadInputs(self):
        for node in self.layers[0].nodes:
            node.inputvalue = random.randint(0,100) # change number when actually allocating it
    def updateConnectionWeights():
        for layer in self.layers:
            for node in layer.nodes:
                for connection in layer.outputs:
                    # do some magic shit
                    pass
    def __init__(self, layers):
        self.metalayers = layers
        self.layers = []
        for i in range(len(layers)-1):
            if i == 0:
                mode = "INPUT"
            else:
                mode = "HIDDEN"
            self.layers.append(layer(layers[i],i,mode))
        self.layers.append(layer(layers[-1],len(layers)-1,"OUTPUT"))
        for i in range(len(self.layers)-1):
            for onode in self.layers[i].nodes:
                for inode in self.layers[i+1].nodes: 
                    con = connection(inode,onode)
                    onode.outputs.append(con)
                    inode.inputs.append(con)
                    
    def generateNewNetwork(self):
        nextNet = network(self.metalayers)
        for layer in range(len(self.layers)):
            for node in range(len(self.layers[layer].nodes)):
                for connection in range(len(self.layers[layer].nodes[node].inputs)):
                    nextNet.layers[layer].nodes[node].inputs[connection].weight = self.layers[layer].nodes[node].inputs[connection].weight + random.uniform(-0.5,0.5)
                nextNet.layers[layer].nodes[node].bias = self.layers[layer].nodes[node].bias + random.uniform(-0.5,0.5)
        return nextNet

if True:
    networks = []
    for i in range(10):
        networks.append(network([2,5,1]))
    for generation in range(100000):
        outputs = []
        for net in networks:
            outputs.append((net, net.feedForward()))
        outputs = sorted(outputs, key=lambda x: x[1],reverse=True) # use the fitness function for the sort
        outputCount = len(outputs)
        i = 0
        while i < np.ceil(outputCount / 2):
            del networks[-1]
            outputs.pop(-1)
            i += 1
        
        newNetworks = networks
        networks = tuple(networks)
        for net in networks:
            newNetworks.append(net.generateNewNetwork())
        pp.pprint(outputs[0])
        del networks
        networks = newNetworks
        del newNetworks,outputs,outputCount
        print("\n")
