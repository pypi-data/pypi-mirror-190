import numpy as np
import matplotlib.pyplot as plt

def Train_class(x,y,statue,hidden_layers,hidden_neurons,learning_rate,epoche):

    class NeuralNetwork:
        def __init__(self, inputs, outputs):
            self.inputs = inputs
            self.outputs = outputs
            self.weights = []
            self.weights.append(np.random.rand(self.inputs,hidden_neurons[0]))
            for i in range(1, hidden_layers):
                self.weights.append(np.random.rand(hidden_neurons[i-1],hidden_neurons[i]))
            self.weights.append(np.random.rand(hidden_neurons[-1], self.outputs))

        def sigmoid(self, x):
            return 1 / (1 + np.exp(-x))

        def sigmoid_derivative(self, x):
            return x * (1 - x)

        def forward_pass(self, inputs):
            layer_output = [inputs]
            for i in range(hidden_layers+1):
                layer_output.append(self.sigmoid(np.dot(layer_output[i], self.weights[i])))
            return layer_output

        def train(self, inputs, labels, epochs):
            for i in range(epochs):
                layer_output = self.forward_pass(inputs)
                layer_error = [labels - layer_output[-1]]
                for j in range(hidden_layers, 0, -1):
                    layer_error.insert(0, layer_error[0].dot(self.weights[j].T) * self.sigmoid_derivative(layer_output[j]))
                for j in range(hidden_layers+1):
                    self.weights[j] += learning_rate * np.dot(layer_output[j].T, layer_error[j])

        def predict(self, inputs):
            layer_output = self.forward_pass(inputs)
            return layer_output[-1]

    nn = NeuralNetwork(inputs=len(x[0]),outputs=len(x[0]))

    nn.train(x, y, epoche)
    pred = nn.predict(x)
    if not statue:
        fig, ax = plt.subplots()
        ax.plot(x.T,y.T, '-b', label='Real Temperatures')
        ax.plot(x.T, pred.T, '--r', label='Predicted Temperatures')
        ax.legend()
        plt.show()
    else :
        s=[int(i) for i in input(f"enter {len(x[0])} values :").split()]
        new_input = np.array([s])
        prediction = nn.predict(new_input)
        print("your predict is ",[int(i) for i in  prediction[0]])


def Train_Reg(x,y,statue,hidden_layers,hidden_neurons,learning_rate,epoche):
    class NeuralNetwork:
        def __init__(self, inputs, outputs):
            self.inputs = inputs
            self.outputs = outputs
            self.weights = []
            self.weights.append(np.random.rand(self.inputs, hidden_neurons[0]))
            for i in range(1, hidden_layers):
                self.weights.append(np.random.rand(hidden_neurons[i - 1], hidden_neurons[i]))
            self.weights.append(np.random.rand(hidden_neurons[-1], self.outputs))

        def sigmoid(self, x):
            return 1 / (1 + np.exp(-x))

        def sigmoid_derivative(self, x):
            return x * (1 - x)

        def forward_pass(self, inputs):
            layer_output = [inputs]
            for i in range(hidden_layers + 1):
                layer_output.append(self.sigmoid(np.dot(layer_output[i], self.weights[i])))
            return layer_output

        def train(self, inputs, labels, epochs):
            for i in range(epochs):
                layer_output = self.forward_pass(inputs)
                layer_error = [labels - layer_output[-1]]
                for j in range(hidden_layers, 0, -1):
                    layer_error.insert(0,
                                       layer_error[0].dot(self.weights[j].T) * self.sigmoid_derivative(layer_output[j]))
                for j in range(hidden_layers + 1):
                    self.weights[j] += learning_rate * np.dot(layer_output[j].T, layer_error[j])

        def predict(self, inputs):
            layer_output = self.forward_pass(inputs)
            return layer_output[-1]

    nn = NeuralNetwork(inputs=len(x[0]), outputs=len(y.T))
    nn.train(x, y, epoche)
    pred = nn.predict(x)
    if not statue:
        fig, ax = plt.subplots()
        ax.plot(x, y, '-b', label='Real Temperatures')
        ax.plot(x, pred, '--r', label='Predicted Temperatures')
        ax.legend()
        plt.show()
    else:
        s = [int(i) for i in input(f"enter {len(x[0])} values :").split()]
        new_input = np.array([s])
        pred = nn.predict(new_input)
        print("your predict is ",(round(pred[0,0]*2)/2))



def Train_Reg_or_Class(x, y, statue, hidden_layers, hidden_neurons, learning_rate, epoche):
    if len(x) != len(y):
        y = y.T
        Train_Reg(x, y, statue, hidden_layers, hidden_neurons, learning_rate, epoche)
    else:
        Train_class(x, y, statue, hidden_layers, hidden_neurons, learning_rate, epoche)
