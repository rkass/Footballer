from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import cPickle

ds = SupervisedDataSet(600, 600)
ds2 = SupervisedDataSet(600, 600)

vects = cPickle.load(open('serialized_vectors.p', 'rb'))
vects2 = cPickle.load(open('serialized_unnormalized.p', 'rb'))
for vector in vects:
  ds.addSample(tuple(vector[0]), tuple(vector[0]))
for vector2 in vects2:
  ds2.addSample(tuple(vector2[0]), tuple(vector2[0]))

def trainIt(hidden, d = 0, lr = 0.005):
  if d == 0:
    data = ds
  else:
    data = ds2
  net = buildNetwork(600, hidden, 600)
  trainer = BackpropTrainer(net, dataset = data, learningrate = lr)
  while True:
    print trainer.train()

#returns the reduced form of an input given 
#takes a reversedautoencoder as input
#the input vector and the network[in progress] 
def reduceAll(autoencoder, vector):
  net = autoencoder.pop()
  net.activate(tuple(vector))
  newVector = net['hidden0'].outputbuffer[net['hidden0'].offset]
  if autoencoder == []:
    return newVector
  else
    return reduceOnce(autoencoder, newVector)
