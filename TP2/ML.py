import random

class Neuron:
    def __init__(self, size):
        self.learningFactor = 1
        self.weights = [0]*size
        self.constants = [0]*size
        for i in range(len(self.weights)):
            self.weights[i] = random.randint(-10,10)
            
        for i in range(len(self.constants)):
            self.constants[i] = random.randint(-10,10)
             
    def guess(self, inputs):
        sum = 0
        for i in range(len(self.weights)):
            sum += self.weights[i]*inputs[i] + self.constants[i]
            return self.activationFunction(sum)
            
    def activationFunction(self,guess):
        if guess > 0:
            return 1
        else:
            return 0
            
    def fixWeights(self):
        for i in range(len(self.weights)):
            self.weights[i] += random.randint(-1,1) * self.learningFactor
            self.constants[i] -= random.randint(-1,1) * self.learningFactor
            
class inputNeuron(Neuron):
    
    def __init__(self,size):
        Neuron.__init__(self, size)
    
    def activationFunction(self, guess):
        return guess
        
class hiddenNeuron(Neuron):
    
    def __init__(self,size):
        Neuron.__init__(self, size)
    
    def activationFunction(self, guess):
        return guess
        
class MovementAI:
    def __init__(self):
        self.inputs = []
        for i in range(4): self.inputs += [inputNeuron(1)]
        self.hiddens = []
        for i in range(4): self.hiddens += [hiddenNeuron(4)]
        self.outputs = []
        for i in range(4): self.outputs += [Neuron(4)]
        
        self.x_loc_input = inputNeuron(1)
        self.y_loc_input = inputNeuron(1)
        self.x_dest_input = inputNeuron(1)
        self.y_dest_input = inputNeuron(1)
        self.hidden1 = hiddenNeuron(4)
        self.hidden1 = hiddenNeuron(4)
        self.hidden1 = hiddenNeuron(4)
        self.hidden1 = hiddenNeuron(4)
        self.up = Neuron(4)
        self.down = Neuron(4)
        self.left = Neuron(4)
        self.right = Neuron(4)
    
    def guess(self, inputs):
        inoutputs = []
        hidoutputs = []
        outputs = []
        for i in range(len(self.inputs)):
            inoutputs += [self.inputs[i].guess([inputs[i]])]
        for j in range(len(self.hiddens)):
            hidoutputs += [self.hiddens[j].guess(inoutputs)]
        for k in range(len(self.outputs)):
            outputs += [self.outputs[k].guess(hidoutputs)]
                    
        print (outputs)
        return outputs
        
    def fixWeights(self):
        print("fixing")
        for i in range(4):
            self.inputs[i].fixWeights()
            self.outputs[i].fixWeights()
            self.hiddens[i].fixWeights()
        
movement = MovementAI()
movement.guess([1,2,3,4])
    