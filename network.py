from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from matplotlib.mlab import PCA
import numpy
import cPickle
import random

ds = SupervisedDataSet(600, 600)
ds2 = SupervisedDataSet(600, 600)

vects = cPickle.load(open('serialized_vectors.p', 'rb'))
vects2 = cPickle.load(open('serialized_unnormalized.p', 'rb'))
for vector in vects:
  ds.addSample(tuple(vector[0]), tuple(vector[0]))
for vector2 in vects2:
  ds2.addSample(tuple(vector2[0]), tuple(vector2[0]))

#Returns projected vectors
def pca(minfrac):
  matrix = []
  for vector in vects:
    matrix.append(vector[0])
  print "Matrix Built"
  training = numpy.array(matrix)
  print "Training..."
  results = PCA(training)
  ret = []
  print "Projecting..."
  for vector in vects:
    ret.append(results.project(vector[0], minfrac))
  return ret

def trainIt(hidden, d = 0, lr = 0.005, iters = 100):
  if d == 0:
    data = ds
  else:
    data = ds2
  net = buildNetwork(600, hidden, 600)
  trainer = BackpropTrainer(net, dataset = data, learningrate = lr)
  i = 0
  error = []
  while i < iters:
    x = trainer.train()
    print x
    error.append(x)
    i += 1
  return net, error

#Randomly sets n values in the vect = 0
def corrupt(vect, n):
  samp = random.sample(range(0, len(vect)), n)
  count = 0
  inputVect = []
  while count < len(vect):
    if count in samp:
      inputVect.append(0)
    else:
      inputVect.append(vect[count])
    count += 1
  return inputVect

def trainItd(hidden, corrupted, lr = 0.005, iters = 100):
  net = buildNetwork(600, hidden, 600)
  i = 0
  error = []
  while i < iters:
    vects = cPickle.load(open('serialized_vectors.p', 'rb'))
    ds = SupervisedDataSet(600, 600)
    for vector in vects:
      ds.addSample(tuple(corrupt(vector[0], corrupted)), tuple(vector[0]))
    trainer = BackpropTrainer(net, dataset = ds, learningrate = lr)
    x = trainer.train()
    print x
    error.append(x)
    i += 1
  return net, error
  


#returns the reduced form of an input given 
#takes a reversedautoencoder as input
#the input vector and the network[in progress] 
def reduceAll(autoencoder, vector):
  net = autoencoder.pop()
  net.activate(tuple(vector))
  newVector = net['hidden0'].outputbuffer[net['hidden0'].offset]
  print "onceThrough"
  if autoencoder == []:
    return newVector
  else:
    return reduceAll(autoencoder, newVector)

def reduceAll2(autoencoder, vector):
  net = autoencoder
  net.activate(tuple(vector))
  newVector = net['hidden0'].outputbuffer[net['hidden0'].offset]
  return newVector
  
def trainMultiple(autoencoder, iters = 5, lr = 0.005, corrupted = 0):
  reduced = []
  au = autoencoder
  for v, vect2 in vects:
    reduced.append(reduceAll2(au, v))
  net = buildNetwork(300, 150, 300)
  i = 0
  error = []
  ds = SupervisedDataSet(300, 300)
  for vect in reduced:
    if corrupted > 0:
      ds.addSample(tuple(corrupt(vect, corrupted)), tuple(vect))
    else:
      ds.addSample(tuple(vect), tuple(vect))
  error = []
  trainer = BackpropTrainer(net, dataset= ds, learningrate = lr)
  count = 1
  while count < iters:
    x = trainer.train()
    print x
    count += 1
    error.append(x)
  return net, error
  
