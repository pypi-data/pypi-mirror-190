from math import exp
from random import random

def initialize_network(n_inputs, hiddens_layer, n_outputs):
	network = list()
	
	hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(hiddens_layer[0])]
	network.append(hidden_layer)
	
	for layer in hiddens_layer[1:]:
		hidden_layer = [{'weights':[random() for i in range(len(network[-1])+1)]} for i in range(layer)]
		network.append(hidden_layer)
		
	output_layer = [{'weights':[random() for i in range(hiddens_layer[-1] + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	
	return network

def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation

def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))

def forward_propagate(network, row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = transfer(activation)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs

def transfer_derivative(output):
	return output * (1.0 - output)

def backward_propagate_error(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

def update_weights(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] += l_rate * neuron['delta']

def train_network(network, train, l_rate, n_epoch, n_outputs, err_val_threshold=0):
	errors = []
	for epoch in range(n_epoch):
		sum_error = 0
		for row in train:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(n_outputs)]
			expected[row[-1]] = 1
			sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			backward_propagate_error(network, expected)
			update_weights(network, row, l_rate)
		print('>epoch=%d, lrate=%.1f, error=%.10f' % (epoch, l_rate, sum_error), end='\r')
		errors.append(sum_error)
		if(sum_error < err_val_threshold):
			print('THRESHOLD')
			break
	return errors

def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))

def save(network, filename):
	with open(filename, 'w') as sv:
		sv.write(str(network))
		sv.close()


def load(filename):
	with open(filename, 'r') as sv:
		data = sv.read()
		sv.close()
	return eval(data)
